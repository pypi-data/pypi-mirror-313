from __future__ import annotations

import json
from collections.abc import (
    Callable,
    Collection,
    Generator,
    Mapping,
    Sequence,
    Set as AbstractSet,
)
from contextlib import contextmanager
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Final, Literal, cast, final

from py4j.clientserver import ClientServer, JavaParameters, PythonParameters
from py4j.java_collections import JavaMap
from py4j.java_gateway import DEFAULT_ADDRESS, DEFAULT_PORT, JavaGateway, JavaObject
from pydantic import JsonValue, TypeAdapter, ValidationError

# Remove this once the session config serialization logic on the Java side is synchronized with the Python side.
from pydantic_core import to_json  # pylint: disable=undeclared-dependency

from ._constant import Constant
from ._data_type import (
    DataType,
    is_numeric_array_type,
    is_numeric_type,
    parse_data_type,
)
from ._endpoint import EndpointHandler
from ._external_aggregate_table_sql import ExternalAggregateTableSql
from ._identification import (
    ColumnIdentifier,
    ExternalColumnIdentifier,
    ExternalTableIdentifier,
    HierarchyIdentifier,
    Identifiable,
    IdentifierT_co,
    LevelIdentifier,
    MeasureIdentifier,
    TableIdentifier,
    identify,
)
from ._jdbc import H2_DRIVER, get_h2_url, normalize_jdbc_url
from ._operation import (
    ComparisonCondition,
    ComparisonOperator,
    Condition,
    ConditionCombinationOperatorBound,
    ConditionComparisonOperatorBound,
    IsinCondition,
    combine_conditions,
    decombine_condition,
)
from ._py4j_utils import (
    to_java_list,
    to_java_map,
    to_java_object,
    to_java_object_array,
    to_java_set,
    to_java_string_array,
    to_python_dict,
    to_python_list,
    to_python_set,
    to_store_field,
)
from ._pydantic import get_type_adapter
from ._report import LoadingReport, _warn_new_errors
from ._transaction import is_transacting_data, is_transacting_data_model, transact_data
from .aggregate_provider import AggregateProvider
from .data_load import DataLoad
from .data_load.csv_load import _PLUGIN_KEY as _CSV_LOAD_PLUGIN_KEY
from .data_stream import DataStream
from .directquery._external_aggregate_table._external_measure import ExternalMeasure
from .directquery._external_aggregate_table.external_aggregate_table import (
    ExternalAggregateTable,
)
from .directquery._external_table_update import (
    ExternalTableUpdate,
    _ExternalTableUpdateChangeType,
    _ExternalTableUpdatePerimeter,
)
from .order import CustomOrder, NaturalOrder
from .order._order import Order
from .session_config import (
    KerberosConfig,
    LdapConfig,
    OidcConfig,
    SecurityConfig,
    SessionConfig,
)

_JavaExternalTableChangeType = Literal[
    "ADD_ROWS",
    "UPDATE_ROWS",
    "REMOVE_ROWS",
    "MIXED_CHANGES",
]
_EXTERNAL_TABLE_UPDATE_CHANGE_TYPE_TO_JAVA_CHANGE_TYPE: dict[
    _ExternalTableUpdateChangeType,
    _JavaExternalTableChangeType,
] = {
    "add": "ADD_ROWS",
    "update": "UPDATE_ROWS",
    "remove": "REMOVE_ROWS",
    "mixed": "MIXED_CHANGES",
}


def _parse_measure_data_type(value: str, /) -> DataType:
    parts = value.split("nullable ")
    return parse_data_type(parts[-1])


def _to_data_type(java_type: Any, /) -> DataType:
    return parse_data_type(java_type.getJavaType())


def _get_level_arguments(
    java_levels: Any,
) -> dict[str, tuple[ColumnIdentifier, DataType]]:
    return {
        name: (
            ColumnIdentifier(
                TableIdentifier(java_level.getTableName()),
                java_level.getFieldName(),
            ),
            _to_data_type(java_level.type()),
        )
        for name, java_level in to_python_dict(java_levels).items()
    }


def _convert_store_field_to_column_identifier(store_field: Any, /) -> ColumnIdentifier:
    return ColumnIdentifier(
        TableIdentifier(store_field.getStore()),
        store_field.getName(),
    )


def _convert_java_column_types(schema: Any, /) -> dict[str, DataType]:
    field_names = list(schema.fieldNames())
    field_types = list(schema.types())
    return {
        field_names[i]: _to_data_type(field_types[i]) for i in range(len(field_names))
    }


_CombinedIsinConstantCondition = Condition[
    IdentifierT_co,
    Literal["eq", "isin"],
    Constant,
    Literal["and"] | None,
]


def _convert_java_mapping_to_combined_isin_constant_condition(
    mapping: Mapping[str, Any],
    /,
    *,
    identify: Callable[[str], IdentifierT_co],
) -> _CombinedIsinConstantCondition[IdentifierT_co] | None:
    if not mapping:
        return None

    return combine_conditions(
        (
            [
                IsinCondition(level_identifier, values).normalized
                for level_identifier, values in {
                    identify(key): {
                        Constant.of(element) for element in to_python_list(elements)
                    }
                    for key, elements in mapping.items()
                }.items()
            ],
        ),
    )


_REALTIME_SOURCE_KEYS = ["KAFKA"]


@final
class JavaApi:
    @contextmanager
    @staticmethod
    def create(
        *,
        address: str | None,
        detached: bool,
        distributed: bool,
        py4j_auth_token: str | None,
        py4j_java_port: int | None,
        session_id: str,
    ) -> Generator[JavaApi, None, None]:
        if address is None:
            address = DEFAULT_ADDRESS

        if py4j_java_port is None:
            py4j_java_port = DEFAULT_PORT

        # Connect to the Java side using the provided Java port and start the Python callback server with a dynamic port.
        gateway = ClientServer(
            java_parameters=JavaParameters(
                address=address,
                auth_token=py4j_auth_token,
                port=py4j_java_port,
            ),
            python_parameters=PythonParameters(daemonize=True, port=0),
        )

        try:
            # Retrieve the port on which the python callback server was bound to.
            cb_server = gateway.get_callback_server()
            assert cb_server
            python_port = cb_server.get_listening_port()

            # Tell the Java side to connect to the Python callback server with the new Python port.
            gateway_server = gateway.java_gateway_server
            assert gateway_server is not None
            gateway_server.resetCallbackClient(  # pyright: ignore[reportCallIssue, reportOptionalCall]
                gateway_server.getCallbackClient().getAddress(),  # pyright: ignore[reportCallIssue, reportOptionalCall]
                python_port,
            )

            java_session: Any = gateway.entry_point
            java_session.api(distributed)
            yield JavaApi(gateway=gateway, session_id=session_id)
        finally:
            if not detached:
                gateway.shutdown()

    def __init__(self, *, gateway: JavaGateway, session_id: str):
        self.gateway: Final = gateway
        self._session_id: Final = session_id

    @property
    def jvm(self) -> Any:
        return self.gateway.jvm

    @property
    def java_api(self) -> Any:
        return self.java_session.api()

    @property
    def java_session(self) -> Any:
        return self.gateway.entry_point

    def refresh(self) -> None:
        if is_transacting_data_model():
            raise NotImplementedError(
                "This operation is not supported inside data model transactions yet.",
            )

        self.java_api.refresh()
        _warn_new_errors(self.get_new_load_errors())

    def _get_java_external_table_update_condition(
        self,
        perimeter: _ExternalTableUpdatePerimeter | None,
        /,
    ) -> JavaObject:
        if isinstance(perimeter, Condition):
            decombined_conditions = decombine_condition(  # type: ignore[var-annotated]
                perimeter,
                allowed_isin_element_types=(Constant,),
                allowed_subject_types=(ColumnIdentifier,),
                allowed_target_types=(Constant,),
            )

            or_conditions: list[JavaObject] = []

            for or_condition in decombined_conditions:
                and_conditions: list[JavaObject] = []

                comparison_conditions, isin_conditions, *_ = or_condition

                for comparison_condition in comparison_conditions:
                    java_condition = self.jvm.com.activeviam.directquery.application.api.refresh.condition.ConditionFactory.equal(
                        comparison_condition.subject.column_name,
                        to_java_object(
                            comparison_condition.target.value,
                            gateway=self.gateway,
                        ),
                    )
                    if comparison_condition.operator == "ne":
                        java_condition = getattr(
                            self.jvm.com.activeviam.directquery.application.api.refresh.condition.ConditionFactory,
                            "not",
                        )(java_condition)
                    else:
                        assert comparison_condition.operator == "eq"

                    and_conditions.append(java_condition)

                and_conditions.extend(
                    getattr(
                        self.jvm.com.activeviam.directquery.application.api.refresh.condition.ConditionFactory,
                        "in",
                    )(
                        to_java_object(
                            isin_condition.subject.column_name,
                            gateway=self.gateway,
                        ),
                        to_java_set(
                            {constant.value for constant in isin_condition.elements},
                            gateway=self.gateway,
                        ),
                    )
                    for isin_condition in isin_conditions
                )

                or_conditions.append(
                    getattr(
                        self.jvm.com.activeviam.directquery.application.api.refresh.condition.ConditionFactory,
                        "and",
                    )(to_java_list(and_conditions, gateway=self.gateway)),
                )

            return getattr(
                self.jvm.com.activeviam.directquery.application.api.refresh.condition.ConditionFactory,
                "or",
            )(to_java_list(or_conditions, gateway=self.gateway))

        return self.jvm.com.activeviam.directquery.application.api.refresh.condition.ConditionFactory.allRows()

    def _get_java_external_table_update(
        self,
        table_update: ExternalTableUpdate,
        /,
    ) -> JavaObject:
        table_name = identify(table_update.table).table_name
        if table_update.change_type == "infer":
            java_change_type: _JavaExternalTableChangeType = "ADD_ROWS"
            return self.jvm.com.activeviam.directquery.application.api.refresh.TableUpdateDetail.create(
                table_name,
                self.jvm.com.activeviam.directquery.application.api.refresh.ChangeType.valueOf(
                    java_change_type,
                ),
                self.jvm.com.activeviam.directquery.application.api.refresh.condition.ConditionFactory.unknown(),
            )

        return self.jvm.com.activeviam.directquery.application.api.refresh.TableUpdateDetail.create(
            table_name,
            self.jvm.com.activeviam.directquery.application.api.refresh.ChangeType.valueOf(
                _EXTERNAL_TABLE_UPDATE_CHANGE_TYPE_TO_JAVA_CHANGE_TYPE[
                    table_update.change_type
                ],
            ),
            self._get_java_external_table_update_condition(table_update.perimeter),
        )

    def _get_change_description(self, *updates: ExternalTableUpdate) -> JavaObject:
        java_table_updates = [
            self._get_java_external_table_update(update) for update in updates
        ]
        return self.jvm.com.activeviam.directquery.application.api.refresh.ChangeDescription.create(
            to_java_list(java_table_updates, gateway=self.gateway),
        )

    def incremental_refresh(self, *updates: ExternalTableUpdate) -> None:
        change_description = self._get_change_description(*updates)
        self.java_api.refresh(change_description)

    @property
    def license_end_date(self) -> datetime:
        return datetime.fromtimestamp(self.java_session.getLicenseEndDate() / 1000)

    @property
    def is_community_license(self) -> bool:
        return cast(bool, self.java_session.isCommunityLicense())

    def publish_measures(self, cube_name: str, /) -> None:
        measures_metada_only = is_transacting_data_model()
        self._outside_transaction_api().publishMeasures(cube_name, measures_metada_only)

    def clear_session(self) -> None:
        self.java_api.clearSession()

    def get_session_port(self) -> int:
        return int(self.java_session.getPort())

    def get_readiness(self) -> bool:
        ready = self.java_api.isReady()
        assert isinstance(ready, bool)
        return ready

    def set_readiness(self, ready: bool, /) -> None:  # noqa: FBT001
        self.java_api.setReadiness(ready)

    def generate_jwt(self) -> str:
        """Return the JWT required to authenticate against to this session."""
        return cast(str, self.java_session.generateJwt())

    def create_endpoint(
        self,
        *,
        http_method: Literal["POST", "GET", "PUT", "DELETE"],
        route: str,
        handler: EndpointHandler,
    ) -> None:
        """Create a new custom endpoint."""
        self._outside_transaction_api().createEndpoint(
            http_method,
            route,
            handler,
        )

    def set_locale(self, locale: str, /) -> None:
        """Set the locale to use for the session."""
        self._enterprise_api().setLocale(locale)

    def export_i18n_template(self, path: Path, /) -> None:
        """Generate a template translations file at the desired location."""
        self._enterprise_api().exportI18nTemplate(str(path))

    def start_application(self, config: SessionConfig, /) -> None:  # noqa: C901, PLR0912
        config_data: dict[str, object] = {}

        if config.app_extensions:
            config_data["app_extensions"] = get_type_adapter(
                dict[str, Path],
            ).dump_python({**config.app_extensions})

        if config.auto_distribution:
            config_data["auto_distribution_config"] = get_type_adapter(
                type(config.auto_distribution),
            ).dump_python(config.auto_distribution)

        if config.branding:
            config_data["branding"] = get_type_adapter(
                type(config.branding),
            ).dump_python(config.branding)

        if config.i18n:
            config_data["i18n"] = get_type_adapter(type(config.i18n)).dump_python(
                config.i18n,
            )

        if config.logging:
            config_data["logging"] = get_type_adapter(type(config.logging)).dump_python(
                config.logging,
            )

        config_data["ready"] = config.ready

        if config.security:
            if config.security.client_certificate:
                config_data["client_certificate"] = get_type_adapter(
                    type(config.security.client_certificate),
                ).dump_python(config.security.client_certificate)

            if config.security.https:
                config_data["https"] = get_type_adapter(
                    type(config.security.https),
                ).dump_python(config.security.https)

            if config.security.jwt and config.security.jwt.key_pair:
                config_data["jwt"] = get_type_adapter(
                    type(config.security.jwt),
                ).dump_python(config.security.jwt)

            if config.security.same_site != SecurityConfig().same_site:
                config_data["same_site"] = get_type_adapter(
                    type(config.security.same_site),
                ).dump_python(config.security.same_site)

            authentication: dict[str, object] = {}

            match config.security.sso:
                case KerberosConfig():
                    authentication["kerberos"] = get_type_adapter(
                        type(config.security.sso),
                    ).dump_python(config.security.sso)
                case LdapConfig():
                    authentication["ldap"] = get_type_adapter(
                        type(config.security.sso),
                    ).dump_python(config.security.sso)
                case OidcConfig():
                    oidc_config = get_type_adapter(
                        type(config.security.sso),
                    ).dump_python(config.security.sso)

                    # See https://github.com/activeviam/activepivot/blob/5ea766c9af9fbce31919112ef493072749569fcd/atoti/patachou/server/server-starter/src/main/java/io/atoti/server/starter/api/configuration/authentication/OidcAuthenticationConfig.java#L42
                    oidc_config["access_token_aud"] = oidc_config[
                        "access_token_allowed_audience"
                    ]
                    del oidc_config["access_token_allowed_audience"]

                    # See https://github.com/activeviam/activepivot/blob/5ea766c9af9fbce31919112ef493072749569fcd/atoti/patachou/server/server-starter/src/main/java/io/atoti/server/starter/api/configuration/authentication/OidcAuthenticationConfig.java#L45.
                    if oidc_config["access_token_issuer_claim"] != "issuer":  # noqa: S105
                        oidc_config["access_token_issuer_url_config_metadata_key"] = (
                            oidc_config["access_token_issuer_claim"]
                        )
                    del oidc_config["access_token_issuer_claim"]

                    authentication["oidc"] = oidc_config
                case None:
                    # Ideally, the basic authentication config would be taken into account even when sso is configured.
                    authentication["basic"] = get_type_adapter(
                        type(config.security.basic_authentication),
                    ).dump_python(
                        config.security.basic_authentication,
                    )

            config_data["authentication"] = authentication

        if config.user_content_storage:
            if isinstance(config.user_content_storage, Path):
                config_data["user_content_storage"] = {
                    "url": normalize_jdbc_url(get_h2_url(config.user_content_storage)),
                    "driver": H2_DRIVER,
                    "hibernate_options": {},
                }
            else:
                config_data["user_content_storage"] = get_type_adapter(
                    type(config.user_content_storage),
                ).dump_python(config.user_content_storage, by_alias=True)

        json_config = to_json(config_data).decode()
        self.java_session.startServer(json_config)

    def _create_java_data_types(
        self,
        data_types: Mapping[str, DataType],
        /,
        *,
        default_values: Mapping[str, Constant | None],
        keys: AbstractSet[str],
    ) -> JavaMap:
        TypeImpl: Any = self.jvm.io.atoti.runtime.api.loading.impl.TypeImpl  # noqa: N806

        java_types: dict[str, object] = {}

        for column_name, data_type in data_types.items():
            if column_name in default_values:
                default_value = default_values[column_name]
                nullable = default_value is None
                java_types[column_name] = (
                    TypeImpl(
                        data_type,
                        nullable,
                    )
                    if default_value is None
                    else TypeImpl(
                        data_type,
                        nullable,
                        to_java_object(default_value.value, gateway=self.gateway),
                    )
                )
            else:
                is_numeric_column = is_numeric_type(data_type) or is_numeric_array_type(
                    data_type,
                )
                java_types[column_name] = TypeImpl(
                    data_type,
                    is_numeric_column and column_name not in keys,
                )

        return to_java_map(java_types, gateway=self.gateway)

    def _outside_transaction_api(self) -> Any:
        return self.java_api.outsideTransactionApi(is_transacting_data())

    def _enterprise_api(self) -> Any:
        return self.java_api.enterpriseApi(is_transacting_data())

    def _create_table_parameters(
        self,
        *,
        data_types: Mapping[str, DataType],
        default_values: Mapping[str, Constant | None],
        is_parameter_table: bool,
        keys: Sequence[str],
        partitioning: str | None,
    ) -> JavaObject:
        return self.jvm.io.atoti.runtime.api.loading.impl.StoreParams(
            to_java_list(keys, gateway=self.gateway),
            partitioning,
            self._create_java_data_types(
                data_types,
                default_values=default_values,
                keys=set(keys),
            ),
            is_parameter_table,
        )

    def create_table(
        self,
        identifier: TableIdentifier,
        /,
        *,
        data_types: Mapping[str, DataType],
        default_values: Mapping[str, Constant | None],
        is_parameter_table: bool,
        keys: Sequence[str],
        partitioning: str | None,
    ) -> None:
        table_params = self._create_table_parameters(
            data_types=data_types,
            default_values=default_values,
            is_parameter_table=is_parameter_table,
            keys=keys,
            partitioning=partitioning,
        )
        self._outside_transaction_api().createStore(identifier.table_name, table_params)
        self.refresh()

    def _convert_load_options(self, options: Mapping[str, object], /) -> JavaMap:
        java_options = {}
        for option in options:
            value = options[option]
            if isinstance(value, Mapping):
                value = to_java_map(value, gateway=self.gateway)
            elif isinstance(value, Collection) and not isinstance(value, str):
                value = to_java_list(value, gateway=self.gateway)
            java_options[option] = value
        return to_java_map(java_options, gateway=self.gateway)

    def infer_data_types(self, data: DataLoad, /) -> dict[str, DataType]:
        keys: Sequence[str] = []
        default_values: Mapping[str, DataType] = {}
        java_options = self._convert_load_options(data._options)
        java_data_types = to_python_dict(
            self._outside_transaction_api()
            .discoverCsvFileFormat(
                to_java_list(keys, gateway=self.gateway),
                to_java_map(default_values, gateway=self.gateway),
                java_options,
            )
            .getTypes()
            if data._plugin_key == _CSV_LOAD_PLUGIN_KEY
            else self._outside_transaction_api().inferTypesFromDataSource(
                data._plugin_key,
                to_java_list(keys, gateway=self.gateway),
                to_java_map(default_values, gateway=self.gateway),
                java_options,
            ),
        )
        return {
            column_name: _to_data_type(java_data_type)
            for column_name, java_data_type in java_data_types.items()
        }

    def load_data_into_table(
        self,
        data: DataLoad | DataStream,
        /,
        *,
        scenario_name: str | None,
        table_identifier: TableIdentifier,
    ) -> None:
        java_options = self._convert_load_options(data._options)
        self.java_api.loadDataSourceIntoStore(
            table_identifier.table_name,
            data._plugin_key,
            self.jvm.io.atoti.runtime.api.loading.impl.LoadingParams().setBranch(
                scenario_name,
            ),
            java_options,
            is_transacting_data(),
        )
        _warn_new_errors(self.get_new_load_errors())

    def create_scenario(
        self,
        scenario_name: str,
        /,
        *,
        parent_scenario_name: str | None,
    ) -> None:
        self._outside_transaction_api().createBranch(
            scenario_name,
            parent_scenario_name,
        )

    def get_scenarios(self) -> set[str]:
        return to_python_set(self.java_api.getBranches())

    def delete_scenario(self, scenario: str, /) -> None:
        if self._outside_transaction_api().deleteBranch(scenario).isEmpty():
            raise ValueError("Cannot delete the default scenario")

    def start_data_transaction(
        self,
        *,
        scenario_name: str | None,
        initiated_by_user: bool,
    ) -> str:
        return str(self.java_api.startTransaction(scenario_name, initiated_by_user))

    def end_data_transaction(
        self,
        transaction_id: str,
        /,
        *,
        has_succeeded: bool,
    ) -> None:
        self.java_api.endTransaction(has_succeeded, int(transaction_id))

    def get_aggregates_cache_capacity(self, cube_name: str, /) -> int:
        java_cache_description = (
            self._outside_transaction_api().getAggregatesCacheDescription(cube_name)
        )
        return cast(int, java_cache_description.getSize())

    def set_aggregates_cache_capacity(self, cube_name: str, capacity: int, /) -> None:
        self._outside_transaction_api().setAggregatesCache(cube_name, capacity)

    def _convert_combined_isin_condition_constant_condition_to_java_map(
        self,
        condition: _CombinedIsinConstantCondition[IdentifierT_co] | None,
        /,
        *,
        identifier_type: type[IdentifierT_co],
        get_key: Callable[[IdentifierT_co], object],
    ) -> JavaMap:
        result: dict[IdentifierT_co, AbstractSet[Constant]] = {}

        if condition is not None:
            comparison_conditions, isin_conditions, _ = decombine_condition(
                condition,
                allowed_subject_types=(identifier_type,),
                allowed_comparison_operators=("eq",),
                allowed_target_types=(Constant,),
                allowed_combination_operators=("and",),
                allowed_isin_element_types=(Constant,),
            )[0]

            for comparison_condition in comparison_conditions:
                result[comparison_condition.subject] = {comparison_condition.target}

            for isin_condition in isin_conditions:
                result[isin_condition.subject] = isin_condition.elements

        return to_java_map(
            {
                get_key(identifier): to_java_list(
                    [
                        to_java_object(constant.value, gateway=self.gateway)
                        for constant in constants
                    ],
                    gateway=self.gateway,
                )
                for identifier, constants in result.items()
            },
            gateway=self.gateway,
        )

    def _convert_python_aggregate_provider_to_java(
        self,
        aggregate_provider: AggregateProvider,
        /,
    ) -> JavaObject:
        java_levels = to_java_list(
            [identify(level)._java_description for level in aggregate_provider.levels],
            gateway=self.gateway,
        )

        java_measures = to_java_list(
            [identify(measure).measure_name for measure in aggregate_provider.measures],
            gateway=self.gateway,
        )

        java_filters = (
            self._convert_combined_isin_condition_constant_condition_to_java_map(
                aggregate_provider.filter,
                identifier_type=LevelIdentifier,
                get_key=lambda identifier: identifier._java_description,
            )
        )

        return (
            self.jvm.io.atoti.runtime.api.impl.AggregateProviderDescription.builder()
            .pluginKey(aggregate_provider.key.upper())
            .levelDescriptions(java_levels)
            .measures(java_measures)
            .partitioning(aggregate_provider.partitioning)
            .filters(java_filters)
            .build()
        )

    def get_aggregate_providers_attributes(
        self,
        /,
        *,
        cube_name: str,
        key: str | None,
    ) -> dict[str, AggregateProvider]:
        java_providers = self._outside_transaction_api().getAggregateProviders(
            cube_name,
        )
        return {
            name: AggregateProvider(
                key=description.pluginKey().lower(),
                levels=[
                    LevelIdentifier._parse_java_description(level)
                    for level in to_python_list(description.levelDescriptions())
                ],
                measures=[
                    MeasureIdentifier(measure_name)
                    for measure_name in to_python_list(description.measures())
                ],
                partitioning=description.partitioning(),
                filter=_convert_java_mapping_to_combined_isin_constant_condition(
                    to_python_dict(description.filters()),
                    identify=lambda key: LevelIdentifier._parse_java_description(key),
                ),
            )
            for name, description in to_python_dict(java_providers).items()
            if key is None or name == key
        }

    def add_aggregate_providers(
        self,
        aggregate_providers: Mapping[str, AggregateProvider],
        /,
        *,
        cube_name: str,
    ) -> None:
        self._outside_transaction_api().addAggregateProviders(
            to_java_map(
                {
                    name: self._convert_python_aggregate_provider_to_java(
                        aggregate_provider,
                    )
                    for name, aggregate_provider in aggregate_providers.items()
                },
                gateway=self.gateway,
            ),
            cube_name,
        )

    def remove_aggregate_providers(
        self,
        names: Collection[str],
        /,
        *,
        cube_name: str,
    ) -> None:
        if not self._outside_transaction_api().removeAggregateProviders(
            to_java_list(
                names,
                gateway=self.gateway,
            ),
            cube_name,
        ):
            raise KeyError(names)

    def _create_java_discovery_config(
        self,
        cube_name: str,
        *,
        allowed_application_names: AbstractSet[str] | None,
        cube_url: str | None,
        cube_port: int | None,
        discovery_protocol_xml: str | None,
    ) -> Any:
        builder = (
            self.jvm.io.atoti.runtime.api.DistributedApi.DiscoveryConfig.builder()
            .cubeName(
                cube_name,
            )
            .catalogName("atoti")
        )

        # Only calling the builder's methods with non `None` values to not override its defaults.
        if allowed_application_names is not None:
            builder = builder.allowedApplicationNames(
                to_java_list(allowed_application_names, gateway=self.gateway),
            )
        if cube_url is not None:
            builder = builder.cubeUrl(cube_url)
        if cube_port is not None:
            builder = builder.cubePort(cube_port)
        if discovery_protocol_xml is not None:
            builder = builder.discoveryProtocolXml(discovery_protocol_xml)

        return builder.build()

    def auto_join_distributed_clusters(self, *, cube_name: str) -> None:
        if not self.is_community_license:
            self._enterprise_api().autoJoinDistributedClusters(cube_name)

    def join_distributed_cluster(
        self,
        *,
        application_name: str,
        query_cube_name: str,
        query_cube_url: str,
        query_cube_port: int | None,
        data_cube_name: str,
        data_cube_url: str | None,
        data_cube_port: int | None,
        discovery_protocol_xml: str | None,
    ) -> None:
        """Join the distributed cluster at the given address for the given distributed cube."""
        query_cube_config = self._create_java_discovery_config(
            query_cube_name,
            allowed_application_names=None,
            cube_port=query_cube_port,
            cube_url=query_cube_url,
            discovery_protocol_xml=None,
        )
        data_cube_config = self._create_java_discovery_config(
            data_cube_name,
            allowed_application_names={application_name},
            cube_port=data_cube_port,
            cube_url=data_cube_url,
            discovery_protocol_xml=discovery_protocol_xml,
        )
        self._enterprise_api().addDataCubeToDistributedCluster(
            query_cube_config,
            data_cube_config,
        )

    def get_table_partitioning(self, identifier: TableIdentifier, /) -> str:
        """Return the table's partitioning."""
        return cast(
            str,
            self._outside_transaction_api().getStorePartitioning(identifier.table_name),
        )

    def get_column_data_type(self, identifier: ColumnIdentifier, /) -> DataType:
        return _to_data_type(
            self.java_api.getFieldType(
                identifier.column_name,
                identifier.table_identifier.table_name,
            ),
        )

    @staticmethod
    def _convert_reports(reports: Collection[Any]) -> list[LoadingReport]:
        """Convert the Java report to Python ones."""
        return [
            LoadingReport(
                name=r.getName(),
                source=r.getType(),
                loaded=r.getLoadedCount(),
                errors=r.getErrorCount(),
                duration=r.getDuration(),
                error_messages=to_python_list(r.getFailureMessages()),
            )
            for r in reports
        ]

    def clear_loading_report(self, identifier: TableIdentifier, /) -> None:
        self.java_api.clearLoadingReports(identifier.table_name)

    def get_loading_report(self, identifier: TableIdentifier, /) -> list[LoadingReport]:
        return self._convert_reports(
            to_python_list(self.java_api.getLoadingReports(identifier.table_name)),
        )

    def get_new_load_errors(self) -> dict[str, int]:
        """Return the new loading errors per table."""
        errors = self.java_api.getNewLoadingErrors()
        return to_python_dict(errors)

    def get_selection_fields(self, cube_name: str, /) -> list[ColumnIdentifier]:
        """Return the list of fields that are part of the cube's datastore selection."""
        java_fields = self._outside_transaction_api().getSelectionFields(cube_name)
        return [
            ColumnIdentifier(
                TableIdentifier(java_field.getStore()),
                java_field.getName(),
            )
            for java_field in to_python_list(java_fields)
        ]

    def create_cube_from_table(
        self,
        cube_name: str,
        /,
        *,
        catalog_names: AbstractSet[str],
        application_name: str,
        table_identifier: TableIdentifier,
        mode: str,
        filter: Condition[  # noqa: A002
            ColumnIdentifier,
            ConditionComparisonOperatorBound,
            Constant | None,
            ConditionCombinationOperatorBound,
        ]
        | None = None,
    ) -> None:
        java_column_conditions = (
            None
            if filter is None
            else self._convert_python_condition_to_java_column_conditions(filter)
        )

        self._outside_transaction_api().createCubeFromStore(
            table_identifier.table_name,
            cube_name,
            to_java_list(catalog_names, gateway=self.gateway),
            application_name,
            mode,
            java_column_conditions,
        )

    def create_distributed_cube(
        self,
        *,
        allowed_application_names: AbstractSet[str],
        cube_name: str,
        cube_url: str | None,
        cube_port: int | None,
        discovery_protocol_xml: str | None,
        distributing_levels: Collection[str],
    ) -> None:
        java_discovery_config = self._create_java_discovery_config(
            cube_name,
            allowed_application_names=allowed_application_names,
            cube_url=cube_url,
            cube_port=cube_port,
            discovery_protocol_xml=discovery_protocol_xml,
        )
        self.java_api.createDistributedCube(
            java_discovery_config,
            to_java_string_array(list(distributing_levels), gateway=self.gateway),
        )

    def delete_cube(self, cube_name: str, /) -> None:
        if not self._outside_transaction_api().deleteCube(cube_name):
            raise KeyError(cube_name)

    def get_table_size(
        self,
        identifier: TableIdentifier,
        /,
        *,
        scenario_name: str | None,
    ) -> int:
        """Get the size of the table on its current scenario."""
        return cast(
            int,
            self._outside_transaction_api().getStoreSize(
                identifier.table_name,
                scenario_name,
            ),
        )

    def _build_java_column_condition(
        self,
        condition: ComparisonCondition[
            ColumnIdentifier,
            ComparisonOperator,
            Constant | None,
        ]
        | IsinCondition[ColumnIdentifier, Constant | None],
        /,
    ) -> JavaObject:
        column_data_type = self.get_column_data_type(condition.subject)

        ColumnCondition = self.jvm.io.atoti.runtime.api.condition.ColumnCondition  # noqa: N806
        comparison_operator_to_java_enum: Mapping[
            ConditionComparisonOperatorBound,
            Any,
        ] = {
            "eq": ColumnCondition.ComparisonOperator.EQ,
            "ne": ColumnCondition.ComparisonOperator.NE,
            "lt": ColumnCondition.ComparisonOperator.LT,
            "le": ColumnCondition.ComparisonOperator.LE,
            "gt": ColumnCondition.ComparisonOperator.GT,
            "ge": ColumnCondition.ComparisonOperator.GE,
            "isin": ColumnCondition.ComparisonOperator.ISIN,
        }

        nullable: Final = True

        return (
            ColumnCondition.builder()
            .storeField(to_store_field(condition.subject, gateway=self.gateway))
            .value(
                to_java_object(
                    None if condition.target is None else condition.target.value,
                    data_type=column_data_type,
                    gateway=self.gateway,
                )
                if isinstance(condition, ComparisonCondition)
                else to_java_object_array(
                    [
                        to_java_object(
                            None if element is None else element.value,
                            gateway=self.gateway,
                            data_type=column_data_type,
                        )
                        for element in condition.elements
                    ],
                    gateway=self.gateway,
                ),
            )
            .comparisonOperator(
                comparison_operator_to_java_enum[
                    condition.operator
                    if isinstance(condition, ComparisonCondition)
                    else "isin"
                ],
            )
            .fieldType(
                self.jvm.io.atoti.runtime.api.loading.impl.TypeImpl(
                    column_data_type,
                    nullable,
                ),
            )
            .build()
        )

    def delete_rows_from_table(
        self,
        identifier: TableIdentifier,
        /,
        *,
        scenario_name: str | None,
        condition: Condition[
            ColumnIdentifier,
            ConditionComparisonOperatorBound,
            Constant | None,
            ConditionCombinationOperatorBound,
        ]
        | None = None,
    ) -> None:
        java_column_conditions = (
            None
            if condition is None
            else self._convert_python_condition_to_java_column_conditions(condition)
        )

        self._inside_transaction(
            lambda: cast(
                None,
                self.java_api.deleteOnStoreBranch(
                    identifier.table_name,
                    scenario_name,
                    java_column_conditions,
                ),
            ),
            scenario_name=scenario_name,
        )

    def update_hierarchies_for_cube(
        self,
        cube_name: str,
        *,
        deleted: Mapping[str, Collection[str]],
        updated: Mapping[str, Mapping[str, Mapping[str, ColumnIdentifier]]],
    ) -> None:
        java_deleted = to_java_map(
            {
                dimension_name: to_java_list(hierarchy_names, gateway=self.gateway)
                for dimension_name, hierarchy_names in deleted.items()
            },
            gateway=self.gateway,
        )
        java_updated = to_java_map(
            {
                dimension_name: to_java_map(
                    {
                        hierarchy_name: to_java_map(
                            {
                                name: to_store_field(column, gateway=self.gateway)
                                for name, column in levels.items()
                            },
                            gateway=self.gateway,
                        )
                        for hierarchy_name, levels in hierarchy.items()
                    },
                    gateway=self.gateway,
                )
                for dimension_name, hierarchy in updated.items()
            },
            gateway=self.gateway,
        )
        self._outside_transaction_api().updateHierarchiesForCube(
            cube_name,
            java_updated,
            java_deleted,
        )

    def create_analysis_hierarchy(
        self,
        name: str,
        /,
        *,
        column_identifier: ColumnIdentifier,
        cube_name: str,
    ) -> None:
        """Create an analysis hierarchy from an existing table column."""
        self._outside_transaction_api().createAnalysisHierarchy(
            cube_name,
            name,
            column_identifier.table_identifier.table_name,
            column_identifier.column_name,
        )

    def create_date_hierarchy(
        self,
        name: str,
        /,
        *,
        cube_name: str,
        column_identifier: ColumnIdentifier,
        levels: Mapping[str, str],
    ) -> None:
        self._outside_transaction_api().createDateHierarchy(
            cube_name,
            column_identifier.table_identifier.table_name,
            column_identifier.column_name,
            name,
            to_java_map(levels, gateway=self.gateway),
        )

    def update_hierarchy_dimension(
        self,
        identifier: HierarchyIdentifier,
        new_dimension: str,
        /,
        *,
        cube_name: str,
    ) -> None:
        self._outside_transaction_api().updateHierarchyCoordinate(
            cube_name,
            identifier._java_description,
            HierarchyIdentifier(
                new_dimension,
                identifier.hierarchy_name,
            )._java_description,
        )

    def update_hierarchy_slicing(
        self,
        identifier: HierarchyIdentifier,
        slicing: bool,  # noqa: FBT001
        /,
        *,
        cube_name: str,
    ) -> None:
        """Update whether the hierarchy is slicing or not."""
        self._outside_transaction_api().setHierarchySlicing(
            cube_name,
            identifier._java_description,
            slicing,
        )

    def update_hierarchy_virtual(
        self,
        identifier: HierarchyIdentifier,
        virtual: bool,  # noqa: FBT001
        /,
        *,
        cube_name: str,
    ) -> None:
        self._outside_transaction_api().setHierarchyVirtual(
            cube_name,
            identifier._java_description,
            virtual,
        )

    def get_hierarchy_properties(
        self,
        identifier: HierarchyIdentifier,
        *,
        cube_name: str,
        key: str | None,
    ) -> dict[str, JsonValue]:
        java_hierarchy = self._outside_transaction_api().getHierarchy(
            cube_name,
            identifier.dimension_name,
            identifier.hierarchy_name,
        )
        if java_hierarchy.isEmpty():
            raise KeyError(identifier.hierarchy_name)
        adapter: TypeAdapter[JsonValue] = get_type_adapter(JsonValue)  # type: ignore[arg-type] # pyright: ignore[reportArgumentType]
        return {
            name: self._read_hierarchy_property(adapter, value)
            for name, value in java_hierarchy.orElseThrow().customProperties().items()
            if key is None or name == key
        }

    def _read_hierarchy_property(
        self,
        adapter: TypeAdapter[JsonValue],
        value: str,
    ) -> JsonValue:
        try:
            return adapter.validate_json(value)
        except ValidationError:
            return value

    def set_hierarchy_properties(
        self,
        identifier: HierarchyIdentifier,
        properties: Mapping[str, JsonValue],
        /,
        *,
        cube_name: str,
    ) -> None:
        self._outside_transaction_api().setHierarchyProperties(
            cube_name,
            identifier.dimension_name,
            identifier.hierarchy_name,
            to_java_map(
                {k: self._encode_hierarchy_property(v) for k, v in properties.items()},
                gateway=self.gateway,
            ),
        )

    @staticmethod
    def _encode_hierarchy_property(value: JsonValue) -> str:
        if isinstance(value, str):
            return value
        return json.dumps(value)

    def update_level_order(
        self,
        identifier: LevelIdentifier,
        order: Order,
        /,
        *,
        cube_name: str,
    ) -> None:
        first_elements = (
            to_java_object_array(order.first_elements, gateway=self.gateway)
            if isinstance(order, CustomOrder)
            else None
        )

        self._outside_transaction_api().updateLevelComparator(
            cube_name,
            identifier._java_description,
            order._key,
            first_elements,
        )

    def set_member_properties(
        self,
        identifier: LevelIdentifier,
        member_properties: Mapping[str, Identifiable[ColumnIdentifier]],
        /,
        *,
        cube_name: str,
    ) -> None:
        java_member_properties = to_java_map(
            {
                name: to_store_field(identify(column), gateway=self.gateway)
                for name, column in member_properties.items()
            },
            gateway=self.gateway,
        )
        self._outside_transaction_api().setMemberProperties(
            cube_name,
            identifier._java_description,
            java_member_properties,
        )

    def get_member_properties(
        self,
        identifier: LevelIdentifier,
        /,
        *,
        cube_name: str,
        key: str | None,
    ) -> dict[str, Identifiable[ColumnIdentifier]]:
        java_member_properties: dict[str, Any] = to_python_dict(
            self._outside_transaction_api().getMemberProperties(
                cube_name,
                identifier._java_description,
            ),
        )
        return {
            name: _convert_store_field_to_column_identifier(store_field)
            for name, store_field in java_member_properties.items()
            if key is None or name is key
        }

    def delete_level(self, identifier: LevelIdentifier, /, *, cube_name: str) -> None:
        if (
            self._outside_transaction_api()
            .removeLevel(identifier._java_description, cube_name)
            .isEmpty()
        ):
            raise KeyError(identifier.level_name)

    def delete_hierarchy(
        self,
        identifier: HierarchyIdentifier,
        /,
        *,
        cube_name: str,
    ) -> None:
        if (
            self._outside_transaction_api()
            .removeHierarchy(identifier._java_description, cube_name)
            .isEmpty()
        ):
            raise KeyError(identifier.hierarchy_name)

    def memory_analysis_export(self, directory: Path, folder: str, /) -> None:
        self._outside_transaction_api().memoryAnalysisExport(str(directory), folder)

    def get_level_column_identifier(
        self,
        identifier: LevelIdentifier,
        /,
        *,
        cube_name: str,
    ) -> ColumnIdentifier:
        java_hierarchy = self._outside_transaction_api().getHierarchy(
            cube_name,
            identifier.hierarchy_identifier.dimension_name,
            identifier.hierarchy_identifier.hierarchy_name,
        )
        assert not java_hierarchy.isEmpty()
        return _get_level_arguments(java_hierarchy.orElseThrow().levels())[
            identifier.level_name
        ][0]

    def get_level_data_type(
        self,
        identifier: LevelIdentifier,
        /,
        *,
        cube_name: str,
    ) -> DataType:
        java_hierarchy = self._outside_transaction_api().getHierarchy(
            cube_name,
            identifier.hierarchy_identifier.dimension_name,
            identifier.hierarchy_identifier.hierarchy_name,
        )
        assert not java_hierarchy.isEmpty()
        return _get_level_arguments(java_hierarchy.orElseThrow().levels())[
            identifier.level_name
        ][1]

    def get_level_order(
        self,
        identifier: LevelIdentifier,
        /,
        *,
        cube_name: str,
    ) -> Order:
        java_hierarchy = (
            self._outside_transaction_api()
            .getHierarchy(
                cube_name,
                identifier.hierarchy_identifier.dimension_name,
                identifier.hierarchy_identifier.hierarchy_name,
            )
            .orElseThrow()
        )
        java_levels = java_hierarchy.levels()
        java_level = next(
            java_level
            for level_name, java_level in to_python_dict(java_levels).items()
            if level_name == identifier.level_name
        )
        comparator_key = java_level.comparatorPluginKey()
        first_elements = (
            list(java_level.firstMembers())
            if java_level.firstMembers() is not None
            else None
        )

        if comparator_key == CustomOrder(first_elements=["unused"])._key:
            assert first_elements is not None
            return CustomOrder(first_elements=first_elements)

        return NaturalOrder(ascending="reverse" not in comparator_key.lower())

    def find_level_hierarchy(
        self,
        level_name: str,
        /,
        *,
        cube_name: str,
        dimension_name: str | None,
        hierarchy_name: str | None,
    ) -> HierarchyIdentifier:
        java_hierarchy = self._outside_transaction_api().findLevelHierarchy(
            cube_name,
            dimension_name,
            hierarchy_name,
            level_name,
        )
        if java_hierarchy.isEmpty():
            raise KeyError(level_name)
        java_hierarchy = java_hierarchy.orElseThrow()
        return HierarchyIdentifier(
            java_hierarchy.dimensionName(),
            java_hierarchy.name(),
        )

    def set_measure_folder(
        self,
        identifier: MeasureIdentifier,
        folder: str | None,
        /,
        *,
        cube_name: str,
    ) -> None:
        self._outside_transaction_api().setMeasureFolder(
            folder,
            identifier.measure_name,
            cube_name,
        )

    def set_measure_formatter(
        self,
        identifier: MeasureIdentifier,
        formatter: str | None,
        /,
        *,
        cube_name: str,
    ) -> None:
        self._outside_transaction_api().setMeasureFormatter(
            formatter,
            identifier.measure_name,
            cube_name,
        )

    def set_measure_visibility(
        self,
        identifier: MeasureIdentifier,
        visible: bool | None,
        /,
        *,
        cube_name: str,
    ) -> None:
        self._outside_transaction_api().setMeasureVisibility(
            visible,
            identifier.measure_name,
            cube_name,
        )

    def set_measure_description(
        self,
        identifier: MeasureIdentifier,
        description: str | None,
        /,
        *,
        cube_name: str,
    ) -> None:
        self._outside_transaction_api().setMeasureDescription(
            description,
            identifier.measure_name,
            cube_name,
        )

    @final
    @dataclass(frozen=True, kw_only=True)
    class JavaMeasureDescription:
        """Description of a measure to build."""

        folder: str
        formatter: str
        visible: bool
        underlying_type: DataType
        description: str | None

    def get_measures(
        self,
        cube_name: str,
        /,
    ) -> dict[MeasureIdentifier, JavaApi.JavaMeasureDescription]:
        """Retrieve the list of the cube's measures, including their required levels."""
        java_measures = self._outside_transaction_api().getMeasures(cube_name)
        measures = to_python_list(java_measures)
        return {
            MeasureIdentifier(measure.name()): JavaApi.JavaMeasureDescription(
                folder=measure.folder(),
                formatter=measure.formatter(),
                visible=measure.visible(),
                underlying_type=_parse_measure_data_type(measure.type()),
                description=measure.description(),
            )
            for measure in measures
        }

    def get_measure(
        self,
        identifier: MeasureIdentifier,
        /,
        *,
        cube_name: str,
    ) -> JavaApi.JavaMeasureDescription:
        measure = self._outside_transaction_api().getMeasure(
            identifier.measure_name,
            cube_name,
        )
        if measure.isEmpty():
            raise KeyError(identifier.measure_name)
        measure = measure.orElseThrow()
        return JavaApi.JavaMeasureDescription(
            folder=measure.folder(),
            formatter=measure.formatter(),
            visible=measure.visible(),
            underlying_type=_parse_measure_data_type(measure.type()),
            description=measure.description(),
        )

    def copy_measure(
        self,
        identifier: MeasureIdentifier,
        new_identifier: MeasureIdentifier,
        /,
        *,
        cube_name: str,
    ) -> None:
        self._outside_transaction_api().copyMeasure(
            cube_name,
            identifier.measure_name,
            new_identifier.measure_name,
        )

    def create_measure(  # pylint: disable=too-many-positional-parameters
        self,
        identifier: MeasureIdentifier | None,
        plugin_key: str,
        /,
        *args: Any,
        cube_name: str,
    ) -> MeasureIdentifier:
        java_args = to_java_object_array(
            [self._levels_to_descriptions(arg) for arg in args],
            gateway=self.gateway,
        )
        name = self._outside_transaction_api().registerMeasure(
            cube_name,
            None if identifier is None else identifier.measure_name,
            plugin_key,
            java_args,
        )
        assert isinstance(name, str)
        return MeasureIdentifier(name)

    def register_aggregation_function(
        self,
        *,
        additional_imports: Collection[str],
        additional_methods: Collection[str],
        contribute_source_code: str,
        decontribute_source_code: str | None,
        merge_source_code: str,
        terminate_source_code: str,
        buffer_types: Collection[DataType],
        output_type: DataType,
        plugin_key: str,
    ) -> None:
        """Register a new user defined aggregation function."""
        self._outside_transaction_api().registerUserDefinedAggregateFunction(
            contribute_source_code,
            decontribute_source_code,
            merge_source_code,
            terminate_source_code,
            to_java_string_array(list(buffer_types), gateway=self.gateway),
            output_type,
            plugin_key,
            to_java_string_array(list(additional_imports), gateway=self.gateway),
            to_java_string_array(list(additional_methods), gateway=self.gateway),
        )

    def _levels_to_descriptions(self, arg: Any) -> Any:
        """Recursively convert levels, hierarchies, and columns to their Java descriptions."""
        if isinstance(arg, tuple):
            return to_java_object_array(
                tuple(self._levels_to_descriptions(e) for e in arg),
                gateway=self.gateway,
            )
        if isinstance(arg, Mapping):
            return to_java_map(
                {
                    self._levels_to_descriptions(k): self._levels_to_descriptions(v)
                    for k, v in arg.items()
                },
                gateway=self.gateway,
            )
        if isinstance(arg, list | set):
            return to_java_list(
                [self._levels_to_descriptions(e) for e in arg],
                gateway=self.gateway,
            )
        if isinstance(arg, ColumnIdentifier):
            return to_store_field(arg, gateway=self.gateway)
        return arg

    def aggregated_measure(
        self,
        identifier: MeasureIdentifier | None,
        plugin_key: str,
        /,
        *,
        cube_name: str,
        column_identifier: ColumnIdentifier,
    ) -> MeasureIdentifier:
        """Create a new aggregated measure and return its name."""
        name = self._outside_transaction_api().createAggregatedMeasure(
            cube_name,
            None if identifier is None else identifier.measure_name,
            column_identifier.table_identifier.table_name,
            column_identifier.column_name,
            plugin_key,
        )
        assert isinstance(name, str)
        return MeasureIdentifier(name)

    def delete_measure(
        self,
        identifier: MeasureIdentifier,
        /,
        *,
        cube_name: str,
    ) -> None:
        if (
            self._outside_transaction_api()
            .removeMeasure(identifier.measure_name, cube_name)
            .isEmpty()
        ):
            raise KeyError(identifier.measure_name)

    def set_column_default_value(
        self,
        identifier: ColumnIdentifier,
        default_value: Constant | None,
        /,
    ) -> None:
        self._outside_transaction_api().setFieldDefaultValue(
            to_java_object(
                None if default_value is None else default_value.value,
                gateway=self.gateway,
            ),
            identifier.column_name,
            identifier.table_identifier.table_name,
        )
        self.refresh()

    def create_parameter_simulation(
        self,
        *,
        cube_name: str,
        simulation_name: str,
        measures: Mapping[MeasureIdentifier, Constant | None],
        level_identifiers: Collection[LevelIdentifier],
        base_scenario_name: str | None,
    ) -> str:
        """Create a simulation in the cube and return the name of its backing table."""
        java_measures = to_java_map(
            {
                measure_identifier.measure_name: None
                if default_value is None
                else default_value.value
                for measure_identifier, default_value in measures.items()
            },
            gateway=self.gateway,
        )
        java_levels = to_java_string_array(
            [
                level_identifier._java_description
                for level_identifier in level_identifiers
            ],
            gateway=self.gateway,
        )
        return cast(
            str,
            self._outside_transaction_api().createParameterSimulation(
                cube_name,
                simulation_name,
                java_levels,
                base_scenario_name,
                java_measures,
            ),
        )

    def _inside_transaction(
        self,
        callback: Callable[[], None],
        *,
        scenario_name: str | None,
        source_key: str | None = None,
    ) -> None:
        if is_transacting_data() or source_key in _REALTIME_SOURCE_KEYS:
            callback()
        else:
            with transact_data(
                allow_nested=True,
                commit=lambda transaction_id: self.end_data_transaction(
                    transaction_id,
                    has_succeeded=True,
                ),
                rollback=lambda transaction_id: self.end_data_transaction(
                    transaction_id,
                    has_succeeded=False,
                ),
                session_id=self._session_id,
                start=lambda: self.start_data_transaction(
                    scenario_name=scenario_name,
                    initiated_by_user=False,
                ),
            ):
                callback()

    def block_until_widget_loaded(self, widget_id: str, /) -> None:
        """Block until the widget is loaded."""
        self.java_api.blockUntilWidgetLoaded(widget_id)

    def get_shared_context_values(
        self,
        /,
        *,
        cube_name: str,
        key: str | None,
    ) -> dict[str, str]:
        return {
            name: value
            for name, value in to_python_dict(
                self._outside_transaction_api().getCubeShareContextValues(cube_name),
            ).items()
            if key is None or name == key
        }

    def set_shared_context_value(
        self,
        key: str,
        value: str,
        /,
        *,
        cube_name: str,
    ) -> None:
        self._outside_transaction_api().setCubeSharedContextValue(cube_name, key, value)

    def set_masking_value(
        self,
        inclusions: Mapping[str, AbstractSet[tuple[Constant, ...]]],
        exclusions: Mapping[str, AbstractSet[tuple[Constant, ...]]],
        /,
        *,
        cube_name: str,
        role: str,
    ) -> None:
        java_inclusions = to_java_map(
            {
                name: to_java_list(
                    [
                        to_java_list(
                            [
                                to_java_object(
                                    path.value,
                                    gateway=self.gateway,
                                    data_type=path.data_type,
                                )
                                for path in members
                            ],
                            gateway=self.gateway,
                        )
                        for members in values
                    ],
                    gateway=self.gateway,
                )
                for name, values in inclusions.items()
            },
            gateway=self.gateway,
        )
        java_exclude = to_java_map(
            {
                name: to_java_list(
                    [
                        to_java_list(
                            [
                                to_java_object(
                                    path.value,
                                    gateway=self.gateway,
                                    data_type=path.data_type,
                                )
                                for path in members
                            ],
                            gateway=self.gateway,
                        )
                        for members in values
                    ],
                    gateway=self.gateway,
                )
                for name, values in exclusions.items()
            },
            gateway=self.gateway,
        )

        self._outside_transaction_api().setCubeMasking(
            cube_name,
            role,
            java_inclusions,
            java_exclude,
        )

    def external_api(self, key: str, /) -> Any:
        return self._outside_transaction_api().externalDatabaseApi(key)

    def _to_java_table_id(self, identifier: ExternalTableIdentifier, /) -> JavaObject:
        return self.jvm.io.atoti.runtime.api.directquery.ExternalTableId(
            identifier.catalog_name,
            identifier.schema_name,
            identifier.table_name,
        )

    def _to_external_table_identifier(
        self,
        java_table_id: Any,
        /,
    ) -> ExternalTableIdentifier:
        return ExternalTableIdentifier(
            java_table_id.databaseName(),
            java_table_id.schemaName(),
            java_table_id.tableName(),
        )

    def connect_to_database(
        self,
        key: str,
        /,
        *,
        url: str | None,
        password: str | None,
        options: Mapping[str, str | None],
    ) -> None:
        options = to_java_map(options, gateway=self.gateway)
        self.external_api(key).connectToDatabase(url, password, options)

    def get_external_tables(
        self,
        key: str,
        /,
    ) -> set[ExternalTableIdentifier]:
        catalogs = self.external_api(key).getTables()
        return {
            ExternalTableIdentifier(
                catalog_name,
                schema_name,
                table_name,
            )
            for catalog_name, schemas in to_python_dict(catalogs).items()
            for schema_name, tables in to_python_dict(schemas).items()
            for table_name in to_python_list(tables)
        }

    def get_external_table_schema(
        self,
        key: str,
        /,
        *,
        identifier: ExternalTableIdentifier,
    ) -> dict[str, DataType]:
        schema = self.external_api(key).getTableSchema(
            self._to_java_table_id(identifier),
        )
        return _convert_java_column_types(schema)

    def add_external_table(
        self,
        key: str,
        /,
        *,
        clustering_columns: AbstractSet[str] | None,
        columns: Mapping[str, str],
        identifier: ExternalTableIdentifier,
        keys: Sequence[str] | None,
        local_table_identifier: TableIdentifier,
    ) -> None:
        java_keys = None if keys is None else to_java_list(keys, gateway=self.gateway)
        java_clustering_columns = (
            None
            if clustering_columns is None
            else to_java_list(clustering_columns, gateway=self.gateway)
        )
        java_columns = to_java_map(columns, gateway=self.gateway)
        self.external_api(key).addTable(
            self._to_java_table_id(identifier),
            local_table_identifier.table_name,
            java_keys,
            java_columns,
            java_clustering_columns,
        )

    def add_external_table_with_multi_row_arrays(
        self,
        key: str,
        /,
        *,
        array_columns: Collection[str],
        clustering_columns: AbstractSet[str] | None,
        identifier: ExternalTableIdentifier,
        columns: Mapping[str, str],
        index_column: str,
        local_table_identifier: TableIdentifier,
    ) -> None:
        java_clustering_columns = (
            None
            if clustering_columns is None
            else to_java_list(clustering_columns, gateway=self.gateway)
        )
        java_columns = to_java_map(columns, gateway=self.gateway)
        self.external_api(key).addTableWithMultiRowArray(
            self._to_java_table_id(identifier),
            local_table_identifier.table_name,
            java_columns,
            java_clustering_columns,
            index_column,
            to_java_list(array_columns, gateway=self.gateway),
        )

    def add_external_multi_column_array_table(
        self,
        key: str,
        /,
        *,
        column_prefixes: Collection[str],
        clustering_columns: AbstractSet[str] | None,
        columns: Mapping[str, str],
        identifier: ExternalTableIdentifier,
        keys: Sequence[str] | None,
        local_table_identifier: TableIdentifier,
    ) -> None:
        java_keys = None if keys is None else to_java_list(keys, gateway=self.gateway)
        java_column_prefixes = to_java_list(column_prefixes, gateway=self.gateway)
        java_clustering_columns = (
            None
            if clustering_columns is None
            else to_java_list(clustering_columns, gateway=self.gateway)
        )
        java_columns = to_java_map(columns, gateway=self.gateway)
        self.external_api(key).addTableWithMultiColumnArray(
            self._to_java_table_id(identifier),
            local_table_identifier.table_name,
            java_keys,
            java_columns,
            java_clustering_columns,
            java_column_prefixes,
        )

    def _convert_python_measure_mapping_to_java(
        self,
        measure_mapping: ExternalMeasure,
        /,
    ) -> Any:
        return (
            self.jvm.io.atoti.runtime.api.directquery.impl.MeasureMappingDescription.builder()
            .aggregationKey(measure_mapping.aggregation_key)
            .originColumns(
                to_java_list(
                    [
                        to_store_field(
                            identify(granular_identifier),
                            gateway=self.gateway,
                        )
                        for granular_identifier in measure_mapping.granular_columns
                    ],
                    gateway=self.gateway,
                ),
            )
            .targetColumns(
                to_java_list(
                    [
                        identify(col).column_name
                        for col in measure_mapping.aggregate_columns
                    ],
                    gateway=self.gateway,
                ),
            )
            .build()
        )

    def _convert_java_measure_mapping_to_python(
        self,
        java_measure_mapping: Any,
        /,
        *,
        aggregate_table_identifier: ExternalTableIdentifier,
    ) -> ExternalMeasure:
        return ExternalMeasure(
            aggregation_key=java_measure_mapping.aggregationKey(),
            granular_columns=[
                _convert_store_field_to_column_identifier(column)
                for column in to_python_list(java_measure_mapping.originColumns())
            ],
            aggregate_columns=[
                ExternalColumnIdentifier(aggregate_table_identifier, column_name)
                for column_name in to_python_list(java_measure_mapping.targetColumns())
            ],
        )

    def _convert_python_external_aggregate_table_to_java(
        self,
        external_aggregate_table: ExternalAggregateTable,
        /,
    ) -> JavaObject:
        granular_table_name = identify(
            external_aggregate_table.granular_table,
        ).table_name
        aggregate_table_id = self._to_java_table_id(
            identify(external_aggregate_table.aggregate_table),
        )
        mapping = to_java_map(
            {
                identify(column): identify(external_column).column_name
                for column, external_column in external_aggregate_table.mapping.items()
            },
            gateway=self.gateway,
        )
        measures = to_java_list(
            [
                self._convert_python_measure_mapping_to_java(measure)
                for measure in external_aggregate_table.measures
            ],
            gateway=self.gateway,
        )
        filters = self._convert_combined_isin_condition_constant_condition_to_java_map(
            external_aggregate_table.filter,
            identifier_type=ColumnIdentifier,
            get_key=lambda identifier: to_store_field(identifier, gateway=self.gateway),
        )
        return (
            self.jvm.io.atoti.runtime.api.directquery.impl.AggregateTableDescription.builder()
            .originBaseTableName(granular_table_name)
            .tableId(aggregate_table_id)
            .groupByFields(mapping)
            .measureMappings(measures)
            .filters(filters)
            .build()
        )

    def _convert_java_external_aggregate_table(
        self,
        description: Any,
        /,
    ) -> ExternalAggregateTable:
        aggregate_table_identifier = self._to_external_table_identifier(
            description.tableId(),
        )
        mapping: Mapping[
            Identifiable[ColumnIdentifier],
            Identifiable[ExternalColumnIdentifier],
        ] = {
            _convert_store_field_to_column_identifier(
                projected_column,
            ): ExternalColumnIdentifier(
                self._to_external_table_identifier(description.tableId()),
                projection_column_name,
            )
            for projected_column, projection_column_name in to_python_dict(
                description.groupByFields(),
            ).items()
        }
        return ExternalAggregateTable(
            granular_table=TableIdentifier(description.originBaseTableName()),
            aggregate_table=aggregate_table_identifier,
            mapping=mapping,
            measures=[
                self._convert_java_measure_mapping_to_python(
                    java_measure_mapping,
                    aggregate_table_identifier=aggregate_table_identifier,
                )
                for java_measure_mapping in to_python_list(
                    description.measureMappings(),
                )
            ],
            filter=_convert_java_mapping_to_combined_isin_constant_condition(
                to_python_dict(description.filters()),
                identify=lambda key: _convert_store_field_to_column_identifier(key),
            ),
        )

    def get_external_aggregate_tables(
        self,
        *,
        key: str | None,
    ) -> dict[str, ExternalAggregateTable]:
        java_aggregate_tables = self._outside_transaction_api().getAggregateTables()
        return {
            name: self._convert_java_external_aggregate_table(description)
            for name, description in to_python_dict(java_aggregate_tables).items()
            if key is None or name == key
        }

    def set_external_aggregate_tables(
        self,
        external_aggregate_tables: Mapping[str, ExternalAggregateTable],
        /,
    ) -> None:
        self._outside_transaction_api().setAggregateTables(
            to_java_map(
                {
                    name: self._convert_python_external_aggregate_table_to_java(
                        aggregate_table,
                    )
                    for name, aggregate_table in external_aggregate_tables.items()
                },
                gateway=self.gateway,
            ),
        )

    def remove_external_aggregate_tables(
        self,
        names: Collection[str],
        /,
    ) -> None:
        self._outside_transaction_api().removeAggregateTables(
            to_java_list(
                names,
                gateway=self.gateway,
            ),
        )

    def derive_external_aggregate_table(
        self,
        provider: AggregateProvider,
        /,
        *,
        cube_name: str,
        key: str,
        table_identifier: ExternalTableIdentifier,
    ) -> ExternalAggregateTable:
        java_aggregate_provider = self._convert_python_aggregate_provider_to_java(
            provider,
        )
        java_aggregate_table = self.external_api(key).deriveAggregateTable(
            cube_name,
            java_aggregate_provider,
            table_identifier.catalog_name,
            table_identifier.schema_name,
            table_identifier.table_name,
        )
        return self._convert_java_external_aggregate_table(java_aggregate_table)

    def generate_external_aggregate_table_sql(
        self,
        aggregate_table: ExternalAggregateTable,
        /,
        *,
        key: str,
    ) -> ExternalAggregateTableSql:
        java_aggregate_table = self._convert_python_external_aggregate_table_to_java(
            aggregate_table,
        )
        java_sql_queries_map = self.external_api(key).getSqlForAggregateTableCreation(
            java_aggregate_table,
        )
        python_sql_queries = {
            key.toString(): value
            for key, value in to_python_dict(java_sql_queries_map).items()
        }
        return ExternalAggregateTableSql(
            create=python_sql_queries["CREATE"],
            insert=python_sql_queries["FEED"],
        )

    def get_external_database_cache(self, key: str, /) -> bool | None:
        return cast(bool | None, self.external_api(key).getCache())

    def set_external_database_cache(self, key: str, /, *, cache: bool) -> None:
        self.external_api(key).setCache(cache)

    def synchronize_with_external_database(self) -> None:
        self.java_api.synchronizeWithDatabase()

    def _convert_python_condition_to_java_column_conditions(
        self,
        condition: Condition[
            ColumnIdentifier,
            ConditionComparisonOperatorBound,
            Constant | None,
            ConditionCombinationOperatorBound,
        ],
    ) -> object:
        return to_java_list(
            [  # type: ignore[var-annotated]
                to_java_list(
                    [
                        self._build_java_column_condition(
                            sub_condition,  # type: ignore[arg-type]
                        )
                        for sub_condition in [
                            *comparison_conditions,
                            *isin_conditions,
                        ]
                    ],
                    gateway=self.gateway,
                )
                for comparison_conditions, isin_conditions, *_ in decombine_condition(
                    condition,
                    allowed_subject_types=(ColumnIdentifier,),
                    allowed_target_types=(Constant, type(None)),
                )
            ],
            gateway=self.gateway,
        )

    def set_hierarchy_dimension_default(
        self,
        identifier: HierarchyIdentifier,
        dimension_default: bool,  # noqa: FBT001
        /,
        *,
        cube_name: str,
    ) -> None:
        self._outside_transaction_api().setHierarchyAsDimensionDefault(
            dimension_default,
            identifier.hierarchy_name,
            identifier.dimension_name,
            cube_name,
        )
