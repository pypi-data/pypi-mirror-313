from __future__ import annotations

from collections import defaultdict
from collections.abc import Set as AbstractSet
from functools import cached_property
from typing import TYPE_CHECKING, Final, Generic, final

from typing_extensions import override

from .._collections import frozendict
from .._data_type import DataType
from .._identification import (
    CatalogName,
    ExternalTableIdentifier,
    ExternalTableKey,
    SchemaName,
)
from .._ipython import ReprJson, ReprJsonable
from ._external_database_connection_config import ExternalDatabaseConnectionConfigT
from .external_table import ExternalTable

if TYPE_CHECKING:
    from .._java_api import JavaApi  # pylint: disable=nested-import


@final
class ExternalTables(Generic[ExternalDatabaseConnectionConfigT], ReprJsonable):
    """Tables of an external database.

    Example:
        .. doctest::
            :hide:

            >>> from atoti._identification import ExternalTableIdentifier
            >>> from atoti.directquery import ExternalTable
            >>> key = "EXAMPLE"
            >>> session = getfixture("default_session")
            >>> external_tables = tt.ExternalTables(
            ...     {ExternalTableIdentifier("my_catalog", "my_schema", "my_table")},
            ...     database_key="unused",
            ...     java_api=session._java_api,
            ... )

        >>> # Individual tables can be accessed with their name only if it is unique:
        >>> external_table = external_tables["my_table"]
        >>> # Or with a tuple with the schema name to differentiate the tables:
        >>> external_table = external_tables["my_schema", "my_table"]
        >>> # Or even a tuple starting with the catalog name:
        >>> external_table = external_tables["my_catalog", "my_schema", "my_table"]

    """

    def __init__(
        self,
        table_identifiers: AbstractSet[ExternalTableIdentifier],
        /,
        *,
        database_key: str,
        java_api: JavaApi,
    ) -> None:
        self._database_key: Final = database_key
        self._java_api: Final = java_api
        self._table_identifiers: Final = table_identifiers

    @cached_property
    def _organized_table_names(
        self,
    ) -> frozendict[CatalogName, frozendict[SchemaName, frozenset[str]]]:
        organized_tables: defaultdict[
            CatalogName,
            defaultdict[SchemaName, set[str]],
        ] = defaultdict(lambda: defaultdict(set))

        for table in self._table_identifiers:
            organized_tables[table.catalog_name][table.schema_name].add(
                table.table_name,
            )

        return frozendict(
            {
                catalog_name: frozendict(
                    {
                        schema_name: frozenset(table_names)
                        for schema_name, table_names in schemas.items()
                    },
                )
                for catalog_name, schemas in organized_tables.items()
            },
        )

    @override
    def _repr_json_(self) -> ReprJson:
        return {
            catalog_name: {
                schema_name: sorted(table_names)
                for schema_name, table_names in schemas.items()
            }
            for catalog_name, schemas in self._organized_table_names.items()
        }, {
            "expanded": False,
            "root": self._database_key,
        }

    def _filter(
        self,
        *,
        catalog_name: str | None = None,
        schema_name: str | None = None,
        table_name: str | None = None,
    ) -> ExternalTables[ExternalDatabaseConnectionConfigT]:
        matching_identifiers = {
            identifier
            for identifier in self._table_identifiers
            if (catalog_name is None or catalog_name == identifier.catalog_name)
            and (schema_name is None or schema_name == identifier.schema_name)
            and (table_name is None or table_name == identifier.table_name)
        }
        return ExternalTables(
            matching_identifiers,
            database_key=self._database_key,
            java_api=self._java_api,
        )

    def __getitem__(
        self,
        table_key: ExternalTableKey,
        /,
    ) -> ExternalTable[ExternalDatabaseConnectionConfigT]:
        identifier = self._resolve_table(table_key)

        def get_data_types() -> dict[str, DataType]:
            return self._java_api.get_external_table_schema(
                self._database_key,
                identifier=identifier,
            )

        return ExternalTable(
            identifier,
            database_key=self._database_key,
            get_data_types=get_data_types,
        )

    def _resolve_table(self, table_key: ExternalTableKey, /) -> ExternalTableIdentifier:
        match table_key:
            case str(table_name):
                catalog_name, schema_name = None, None
            case (schema_name, table_name):
                catalog_name = None
            case (catalog_name, schema_name, table_name):
                ...

        filtered_tables = self._filter(
            catalog_name=catalog_name,
            schema_name=schema_name,
            table_name=table_name,
        )

        schema_message = "" if schema_name is None else f" in schema {schema_name}"
        catalog_message = "" if catalog_name is None else f" in catalog {catalog_name}"

        match list(filtered_tables._table_identifiers):
            case []:
                raise KeyError(
                    f"No table named {table_name}{schema_message}{catalog_message}",
                )
            case [matching_identifier]:
                return matching_identifier
            case _:
                raise KeyError(
                    f"Too many tables named {table_name}{schema_message}{catalog_message}: {filtered_tables._table_identifiers}",
                )
