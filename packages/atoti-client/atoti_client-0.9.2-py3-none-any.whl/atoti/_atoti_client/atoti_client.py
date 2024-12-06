from collections.abc import Callable, Generator, Sequence
from contextlib import AbstractContextManager, contextmanager
from typing import Final, Literal, final, overload

import pandas as pd

from .._activeviam_client import ActiveViamClient
from .._column_description import ColumnDescription
from .._constant import Constant
from .._context import Context
from .._cube_discovery import CubeDiscovery
from .._get_data_types import GetDataTypes
from .._graphql_client import GraphqlClient
from .._identification import (
    ColumnIdentifier,
    LevelIdentifier,
    MeasureIdentifier,
    TableName,
)
from .._operation import (
    Condition,
    ConditionCombinationOperatorBound,
    ConditionComparisonOperatorBound,
)
from .._query_explanation import QueryExplanation
from .._query_filter import QueryFilter
from .._typing import Duration
from ..mdx_query_result import MdxQueryResult
from ._execute_cube_query import execute_cube_query
from ._execute_mdx_query import execute_mdx_query
from ._execute_table_query import execute_table_query
from ._explain_mdx_query import explain_mdx_query
from ._get_cube_discovery import get_cube_discovery

_PIVOT_VERSIONS_WITHOUT_DATA_EXPORT_SERVICE = ("4", "5")


# To prevent this class from becoming huge, methods should be implemented in functions in dedicated modules.
@final
class AtotiClient:
    """Client to interact with Atoti Server through HTTP."""

    def __init__(self, *, activeviam_client: ActiveViamClient) -> None:
        self.activeviam_client: Final = activeviam_client
        self._cache_cube_discovery: bool = False
        self._cached_cube_discovery: CubeDiscovery | None = None
        # This should be `self.graphql_client` but making the attribute public make `pyright --ignoreexternal --verifytypes atoti` fail.
        # Revisit when upgrading pyright.
        self._graphql_client: Final = (
            GraphqlClient(
                url="graphql",
                http_client=activeviam_client.http_client,
            )
            # Using the presence of a compatible `atoti` namespace as a hint for the presence of the GraphQL service to avoid an extra HTTP request.
            if activeviam_client.has_compatible_atoti_python_api_service
            else None
        )

    @property
    def cached_cube_discovery(self) -> AbstractContextManager[None]:
        @contextmanager
        def cached_cube_discovery() -> Generator[None, None, None]:
            if self._cache_cube_discovery:
                yield
            else:
                self._cache_cube_discovery = True
                try:
                    yield
                finally:
                    self._cached_cube_discovery = None
                    self._cache_cube_discovery = False

        return cached_cube_discovery()

    @property
    def has_data_export_service(self) -> bool:
        return any(
            version.id not in _PIVOT_VERSIONS_WITHOUT_DATA_EXPORT_SERVICE
            for version in self.activeviam_client.server_versions.apis[
                self.pivot_namespace
            ].versions
        )

    @property
    def has_gaq_service(self) -> bool:
        return self.activeviam_client.has_compatible_atoti_python_api_service

    @property
    def pivot_namespace(self) -> str:
        return self.activeviam_client.normalize_activeviam_namespace("pivot")

    def execute_cube_query(
        self,
        *,
        context: Context,
        cube_name: str,
        filter: QueryFilter | None,  # noqa: A002
        get_cube_discovery: Callable[[], CubeDiscovery],
        get_data_types: GetDataTypes,
        get_widget_creation_code: Callable[[], str | None],
        include_empty_rows: bool,
        include_totals: bool,
        level_identifiers: Sequence[LevelIdentifier],
        measure_identifiers: Sequence[MeasureIdentifier],
        mode: Literal["pretty", "raw"],
        scenario_name: str | None,
        session_id: str,
        timeout: Duration,
    ) -> pd.DataFrame:
        with self.cached_cube_discovery:
            return execute_cube_query(
                activeviam_client=self.activeviam_client,
                context=context,
                cube_name=cube_name,
                filter=filter,
                get_cube_discovery=get_cube_discovery,
                get_data_types=get_data_types,
                get_widget_creation_code=get_widget_creation_code,
                has_data_export_service=self.has_data_export_service,
                has_gaq_service=self.has_gaq_service,
                include_empty_rows=include_empty_rows,
                include_totals=include_totals,
                level_identifiers=level_identifiers,
                measure_identifiers=measure_identifiers,
                mode=mode,
                pivot_namespace=self.pivot_namespace,
                scenario_name=scenario_name,
                session_id=session_id,
                timeout=timeout,
            )

    @overload
    def execute_mdx_query(
        self,
        *,
        context: Context,
        get_cube_discovery: Callable[[], CubeDiscovery],
        get_data_types: GetDataTypes | None,
        get_widget_creation_code: Callable[[], str | None],
        keep_totals: bool,
        mdx: str,
        mode: Literal["pretty"],
        session_id: str,
        timeout: Duration,
    ) -> MdxQueryResult: ...

    @overload
    def execute_mdx_query(
        self,
        *,
        context: Context,
        get_cube_discovery: Callable[[], CubeDiscovery],
        get_data_types: GetDataTypes | None,
        get_widget_creation_code: Callable[[], str | None],
        keep_totals: bool,
        mdx: str,
        mode: Literal["raw"],
        session_id: str,
        timeout: Duration,
    ) -> pd.DataFrame: ...

    def execute_mdx_query(
        self,
        *,
        context: Context,
        get_cube_discovery: Callable[[], CubeDiscovery],
        get_data_types: GetDataTypes | None,
        get_widget_creation_code: Callable[[], str | None],
        keep_totals: bool,
        mdx: str,
        mode: Literal["pretty", "raw"],
        session_id: str,
        timeout: Duration,
    ) -> MdxQueryResult | pd.DataFrame:
        with self.cached_cube_discovery:
            return execute_mdx_query(
                activeviam_client=self.activeviam_client,
                context=context,
                get_cube_discovery=get_cube_discovery,
                get_data_types=get_data_types,
                get_widget_creation_code=get_widget_creation_code,
                has_data_export_service=self.has_data_export_service,
                keep_totals=keep_totals,
                mdx=mdx,
                mode=mode,
                pivot_namespace=self.pivot_namespace,
                session_id=session_id,
                timeout=timeout,
            )

    def execute_table_query(
        self,
        *,
        column_descriptions: Sequence[ColumnDescription],
        filter: Condition[  # noqa: A002
            ColumnIdentifier,
            ConditionComparisonOperatorBound,
            Constant,
            ConditionCombinationOperatorBound,
        ]
        | None = None,
        max_rows: int,
        scenario_name: str | None,
        table_name: TableName,
        timeout: Duration,
    ) -> pd.DataFrame:
        return execute_table_query(
            activeviam_client=self.activeviam_client,
            column_descriptions=column_descriptions,
            filter=filter,
            max_rows=max_rows,
            scenario_name=scenario_name,
            table_name=table_name,
            timeout=timeout,
        )

    def explain_mdx_query(
        self,
        *,
        context: Context,
        mdx: str,
        timeout: Duration,
    ) -> QueryExplanation:
        return explain_mdx_query(
            activeviam_client=self.activeviam_client,
            context=context,
            mdx=mdx,
            pivot_namespace=self.pivot_namespace,
            timeout=timeout,
        )

    def get_cube_discovery(self) -> CubeDiscovery:
        if self._cached_cube_discovery is not None:
            return self._cached_cube_discovery

        cube_discovery = get_cube_discovery(
            activeviam_client=self.activeviam_client,
            pivot_namespace=self.pivot_namespace,
        )

        if self._cache_cube_discovery:
            self._cached_cube_discovery = cube_discovery

        return cube_discovery
