from collections.abc import Mapping, Set as AbstractSet
from contextlib import AbstractContextManager
from typing import Final, final

import pandas as pd
import pyarrow as pa
from typing_extensions import assert_never, override

from ._arrow_utils import get_data_types_from_arrow
from ._atoti_client import AtotiClient
from ._collections import DelegatingMutableMapping
from ._data_type import DataType
from ._database_schema import DatabaseSchema
from ._doc import doc
from ._graphql_client import DeleteTableInput
from ._identification import TableIdentifier, TableName
from ._ipython import ReprJson, ReprJsonable
from ._java_api import JavaApi
from ._pandas_utils import pandas_to_arrow
from ._transaction import (
    TRANSACTION_DOC_KWARGS as _TRANSACTION_DOC_KWARGS,
    transact_data,
)
from .data_load import DataLoad
from .table import Table, _LoadArgument


@final
class Tables(DelegatingMutableMapping[TableName, Table], ReprJsonable):  # type: ignore[misc]
    r"""Manage the local :class:`~atoti.Table`\ s of a :class:`~atoti.Session`."""

    def __init__(
        self,
        *,
        atoti_client: AtotiClient,
        java_api: JavaApi,
        session_id: str,
    ):
        self._atoti_client: Final = atoti_client
        self._java_api: Final = java_api
        self._session_id: Final = session_id

    def _get_table_identifiers(self, *, key: TableName | None) -> list[TableIdentifier]:
        assert self._atoti_client._graphql_client

        if key is None:
            tables = self._atoti_client._graphql_client.get_tables().data_model.tables
            return [TableIdentifier(table_name=table.name) for table in tables]

        table = self._atoti_client._graphql_client.find_table(
            table_name=key,
        ).data_model.table
        return [TableIdentifier(table_name=table.name)] if table else []

    @override
    def _get_delegate(self, *, key: TableName | None) -> Mapping[TableName, Table]:
        return {
            identifier.table_name: Table(
                identifier,
                atoti_client=self._atoti_client,
                java_api=self._java_api,
                scenario=None,
            )
            for identifier in self._get_table_identifiers(key=key)
        }

    @override
    def _update_delegate(
        self,
        other: Mapping[TableName, Table],
        /,
    ) -> None:
        raise AssertionError(
            "Use `Session.create_table()` or other methods such as `Session.read_pandas()` to create a table.",
        )

    @override
    def _delete_delegate_keys(self, keys: AbstractSet[TableName], /) -> None:
        assert self._atoti_client._graphql_client
        for key in keys:
            self._atoti_client._graphql_client.delete_table(
                DeleteTableInput(table_identifier=TableIdentifier(key)._graphql_input)
            )

    @override
    def _repr_json_(self) -> ReprJson:
        return (
            dict(
                sorted(
                    {
                        table.name: table._repr_json_()[0] for table in self.values()
                    }.items(),
                ),
            ),
            {"expanded": False, "root": "Tables"},
        )

    @doc(
        **_TRANSACTION_DOC_KWARGS,
        countries_table_data_types_argument="""{"City": "String", "Country": "String"}""",
        keys_argument="""{"City"}""",
    )
    def data_transaction(
        self,
        scenario_name: str | None = None,
        *,
        allow_nested: bool = True,
    ) -> AbstractContextManager[None]:
        """Create a data transaction to batch several data loading operations.

        * It is more efficient than doing each :meth:`~atoti.Table.load` one after the other, especially when using :meth:`~atoti.Table.load_async` to load data concurrently in multiple tables.
        * It avoids possibly incorrect intermediate states (e.g. if loading some new data requires dropping existing rows first).

        Note:
            Data transactions cannot be mixed with:

            * Long-running data operations such as :meth:`~atoti.Table.stream`.
            * Data model operations such as :meth:`~atoti.Session.create_table`, :meth:`~atoti.Table.join`, or defining a new measure.
            * Operations on parameter tables created from :meth:`~atoti.Cube.create_parameter_hierarchy_from_members` and :meth:`~atoti.Cube.create_parameter_simulation`.
            * Operations on other source scenarios than the one the transaction is started on.

        Args:
            {allow_nested}
            scenario_name: The name of the source scenario impacted by all the table operations inside the transaction.

        Example:
            .. doctest::
                :hide:

                >>> session = getfixture("default_session")

            >>> cities_df = pd.DataFrame(
            ...     columns=["City", "Price"],
            ...     data=[
            ...         ("Berlin", 150.0),
            ...         ("London", 240.0),
            ...         ("New York", 270.0),
            ...         ("Paris", 200.0),
            ...     ],
            ... )
            >>> cities_table = session.read_pandas(
            ...     cities_df,
            ...     keys={keys_argument},
            ...     table_name="Cities",
            ... )
            >>> extra_cities_df = pd.DataFrame(
            ...     columns=["City", "Price"],
            ...     data=[
            ...         ("Singapore", 250.0),
            ...     ],
            ... )
            >>> with session.tables.data_transaction():
            ...     cities_table += ("New York", 100.0)
            ...     cities_table.drop(cities_table["City"] == "Paris")
            ...     cities_table.load(extra_cities_df)
            >>> cities_table.head().sort_index()
                       Price
            City
            Berlin     150.0
            London     240.0
            New York   100.0
            Singapore  250.0
            >>> cities_table.drop()

            Loading data concurrently in multiple tables:

            >>> import asyncio
            >>> countries_table = session.create_table(
            ...     "Countries",
            ...     data_types={countries_table_data_types_argument},
            ...     keys={keys_argument},
            ... )
            >>> cities_table.join(countries_table)
            >>> countries_df = pd.DataFrame(
            ...     columns=["City", "Country"],
            ...     data=[
            ...         ("Berlin", "Germany"),
            ...         ("London", "England"),
            ...         ("New York", "USA"),
            ...         ("Paris", "France"),
            ...     ],
            ... )
            >>> async def load_data_in_all_tables(tables):
            ...     with tables.data_transaction():
            ...         await asyncio.gather(
            ...             tables["Cities"].load_async(cities_df),
            ...             tables["Countries"].load_async(countries_df),
            ...         )
            >>> cities_table.drop()
            >>> asyncio.run(load_data_in_all_tables(session.tables))
            >>> cities_table.head()
                      Price
            City
            Berlin    150.0
            London    240.0
            New York  270.0
            Paris     200.0
            >>> countries_table.head()
                      Country
            City
            Berlin    Germany
            London    England
            New York      USA
            Paris      France
            >>> cities_table.drop()

            Nested transactions allowed:

            >>> def composable_function(session):
            ...     table = session.tables["Cities"]
            ...     with session.tables.data_transaction():
            ...         table += ("Paris", 100.0)
            >>> # The function can be called in isolation:
            >>> composable_function(session)
            >>> cities_table.head().sort_index()
                   Price
            City
            Paris  100.0
            >>> with session.tables.data_transaction(
            ...     allow_nested=False  # No-op because this is the outer transaction.
            ... ):
            ...     cities_table.drop()
            ...     cities_table += ("Berlin", 200.0)
            ...     # The function can also be called inside another transaction and will contribute to it:
            ...     composable_function(session)
            ...     cities_table += ("New York", 150.0)
            >>> cities_table.head().sort_index()
                      Price
            City
            Berlin    200.0
            New York  150.0
            Paris     100.0

            Nested transactions not allowed:

            >>> def not_composable_function(session):
            ...     table = session.tables["Cities"]
            ...     with session.tables.data_transaction(allow_nested=False):
            ...         table.drop()
            ...         table += ("Paris", 100.0)
            ...     assert table.row_count == 1
            >>> # The function can be called in isolation:
            >>> not_composable_function(session)
            >>> with session.tables.data_transaction():
            ...     cities_table.drop()
            ...     cities_table += ("Berlin", 200.0)
            ...     # This is a programming error, the function cannot be called inside another transaction:
            ...     not_composable_function(session)
            ...     cities_table += ("New York", 150.0)
            Traceback (most recent call last):
                ...
            RuntimeError: Cannot start this transaction inside another transaction since nesting is not allowed.
            >>> # The last transaction was rolled back:
            >>> cities_table.head().sort_index()
                   Price
            City
            Paris  100.0

        See Also:
            :meth:`~atoti.Session.data_model_transaction`.

        """
        return transact_data(
            allow_nested=allow_nested,
            commit=lambda transaction_id: self._java_api.end_data_transaction(
                transaction_id,
                has_succeeded=True,
            ),
            rollback=lambda transaction_id: self._java_api.end_data_transaction(
                transaction_id,
                has_succeeded=False,
            ),
            session_id=self._session_id,
            start=lambda: self._java_api.start_data_transaction(
                scenario_name=scenario_name,
                initiated_by_user=True,
            ),
        )

    def infer_data_types(self, data: _LoadArgument, /) -> dict[str, DataType]:  # pyright: ignore[reportUnknownParameterType]
        """Infer data types from the passed *data*.

        Args:
            data: The data from which data types should be inferred.

        Example:
            .. doctest::
                :hide:

                >>> directory = getfixture("tmp_path")
                >>> session = getfixture("default_session")

            >>> from datetime import date
            >>> dataframe = pd.DataFrame(
            ...     {
            ...         "Id": [1, 2, 3],
            ...         "Name": ["Phone", "Watch", "Laptop"],
            ...         "Price": [849.99, 249.99, 1499.99],
            ...         "Date": [
            ...             date(2024, 11, 27),
            ...             date(2024, 11, 26),
            ...             date(2024, 11, 25),
            ...         ],
            ...     }
            ... )
            >>> session.tables.infer_data_types(dataframe)
            {'Id': 'long', 'Name': 'String', 'Price': 'double', 'Date': 'LocalDate'}

        See Also:
            :meth:`~atoti.Table.load`.
        """
        match data:
            case pa.Table():
                return get_data_types_from_arrow(data)
            case pd.DataFrame():
                arrow_table = pandas_to_arrow(data, data_types={})
                return self.infer_data_types(arrow_table)
            case DataLoad():
                return self._java_api.infer_data_types(data)
            case _:
                assert_never(data)

    @property
    def schema(self) -> object:
        """Schema of the tables represented as a `Mermaid <https://mermaid.js.org>`__ entity relationship diagram.

        Each table is represented with 3 or 4 columns:

        #. whether the column's :attr:`~atoti.Column.default_value` is ``None`` (denoted with :guilabel:`nullable`) or not
        #. the column :attr:`~atoti.Column.data_type`
        #. (optional) whether the column is part of the table :attr:`~atoti.Table.keys` (denoted with :guilabel:`PK`) or not
        #. the column :attr:`~atoti.Column.name`

        Example:
            .. raw:: html

                <div class="mermaid">
                erDiagram
                  "Table a" {
                      _ String "foo"
                      nullable int "bar"
                  }
                  "Table b" {
                      _ int PK "bar"
                      _ LocalDate "baz"
                  }
                  "Table c" {
                      _ String PK "foo"
                      _ double PK "xyz"
                  }
                  "Table d" {
                      _ String PK "foo_d"
                      _ double PK "xyz_d"
                      nullable float "abc_d"
                  }
                  "Table a" }o--o| "Table b" : "`bar` == `bar`"
                  "Table a" }o..o{ "Table c" : "`foo` == `foo`"
                  "Table c" }o--|| "Table d" : "(`foo` == `foo_d`) & (`xyz` == `xyz_d`)"
                </div>

        """
        assert self._atoti_client._graphql_client
        data_model = self._atoti_client._graphql_client.get_database_schema().data_model
        return DatabaseSchema(data_model)
