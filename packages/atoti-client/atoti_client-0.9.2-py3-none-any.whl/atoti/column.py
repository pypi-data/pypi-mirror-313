from __future__ import annotations

from collections.abc import Collection
from functools import cached_property
from typing import Final, Literal, final, overload

from typing_extensions import override

from ._atoti_client import AtotiClient
from ._check_named_object_defined import check_named_object_defined
from ._constant import Constant, ConstantValue
from ._data_type import DataType, data_type_from_graphql
from ._graphql_client import (
    SetColumnDefaultValue,
    UpdateColumnAction,
    UpdateColumnInput,
)
from ._identification import ColumnIdentifier
from ._ipython import ReprJson, ReprJsonable
from ._java_api import JavaApi
from ._operation import Condition, IsinCondition, OperandConvertibleWithIdentifier


@final
class Column(
    OperandConvertibleWithIdentifier[ColumnIdentifier],
    ReprJsonable,
):
    """Column of a :class:`~atoti.Table`."""

    def __init__(
        self,
        identifier: ColumnIdentifier,
        /,
        *,
        atoti_client: AtotiClient,
        java_api: JavaApi,
        table_keys: Collection[str],
    ) -> None:
        self.__identifier: Final = identifier
        self._atoti_client: Final = atoti_client
        self._java_api: Final = java_api
        self._table_keys: Final = table_keys

    @property
    def name(self) -> str:
        """The name of the column."""
        return self._identifier.column_name

    @cached_property
    def _data_type(self) -> DataType:
        assert self._atoti_client._graphql_client
        table = check_named_object_defined(
            self._atoti_client._graphql_client.get_column_data_type(
                column_name=self.name,
                table_name=self._identifier.table_identifier.table_name,
            ).data_model.table,
            "table",
            self._identifier.table_identifier.table_name,
        )
        column = check_named_object_defined(
            table.column,
            "column",
            self.name,
        )
        return data_type_from_graphql(column.data_type)

    @property
    def data_type(self) -> DataType:
        """The type of the elements in the column."""
        return self._data_type

    @property
    @override
    def _identifier(self) -> ColumnIdentifier:
        return self.__identifier

    @property
    @override
    def _operation_operand(self) -> ColumnIdentifier:
        return self._identifier

    @property
    def default_value(self) -> ConstantValue | None:
        """Value used to replace ``None`` inserted values.

        If not ``None``, the default value must match the column's :attr:`~atoti.Column.data_type`.
        For instance, a ``LocalDate`` column cannot use the string ``"N/A"`` as its default value.

        .. doctest::
            :hide:

            >>> session = getfixture("default_session")

        Each data type has its own default ``default_value`` value:

        >>> from pprint import pprint
        >>> table = session.create_table(
        ...     "Main data types",
        ...     data_types={
        ...         data_type: data_type
        ...         for data_type in [
        ...             "boolean",
        ...             "double",
        ...             "double[]",
        ...             "float",
        ...             "float[]",
        ...             "int",
        ...             "int[]",
        ...             "LocalDate",
        ...             "LocalDateTime",
        ...             "LocalTime",
        ...             "long",
        ...             "long[]",
        ...             "String",
        ...             "ZonedDateTime",
        ...         ]
        ...     },
        ... )
        >>> pprint(
        ...     {
        ...         column_name: table[column_name].default_value
        ...         for column_name in table
        ...     },
        ...     sort_dicts=False,
        ... )
        {'boolean': False,
         'double': None,
         'double[]': None,
         'float': None,
         'float[]': None,
         'int': None,
         'int[]': None,
         'LocalDate': datetime.date(1970, 1, 1),
         'LocalDateTime': datetime.datetime(1970, 1, 1, 0, 0),
         'LocalTime': datetime.time(0, 0),
         'long': None,
         'long[]': None,
         'String': 'N/A',
         'ZonedDateTime': datetime.datetime(1970, 1, 1, 0, 0, tzinfo=TzInfo(UTC))}

        Key columns cannot have ``None`` as their default value so it is forced to something else.
        For numeric scalar columns, this is zero:

        >>> table = session.create_table(
        ...     "Numeric",
        ...     data_types={
        ...         data_type: data_type
        ...         for data_type in [
        ...             "int",
        ...             "float",
        ...             "long",
        ...             "double",
        ...         ]
        ...     },
        ...     keys={"int", "float"},
        ... )
        >>> {column_name: table[column_name].default_value for column_name in table}
        {'int': 0, 'float': 0.0, 'long': None, 'double': None}
        >>> table += (None, None, None, None)
        >>> table.head()
                   long  double
        int float
        0   0.0    <NA>    <NA>

        The default value of array columns is ``None`` and cannot be changed:

        >>> session.create_table(  # doctest: +ELLIPSIS
        ...     "Array",
        ...     data_types={"long[]": "long[]"},
        ...     default_values={"long[]": [0, 0]},
        ... )
        Traceback (most recent call last):
            ...
        py4j.protocol.Py4JJavaError: ... there is no global default value defined for this type. ...

        Changing the default value from ``None`` to something else affects both the previously inserted ``None`` values and the upcoming ones:

        >>> table["long"].default_value = 42
        >>> table["long"].default_value
        42
        >>> table.head()
                   long  double
        int float
        0   0.0      42    <NA>
        >>> table += (1, None, None, None)
        >>> table.head().sort_index()
                   long  double
        int float
        0   0.0      42    <NA>
        1   0.0      42    <NA>

        Changing the default value of a column with a non-``None`` default value does not affect the existing rows:

        >>> table["long"].default_value = 1337
        >>> table["long"].default_value
        1337
        >>> table += (2, None, None, None)
        >>> table.head().sort_index()
                   long  double
        int float
        0   0.0      42    <NA>
        1   0.0      42    <NA>
        2   0.0    1337    <NA>
        >>> del session.tables["Numeric"]
        >>> table = session.create_table(
        ...     "Numeric",
        ...     keys={"int", "float"},
        ...     data_types={
        ...         data_type: data_type
        ...         for data_type in [
        ...             "int",
        ...             "float",
        ...             "long",
        ...             "double",
        ...         ]
        ...     },
        ...     default_values={"long": 1337},
        ... )
        >>> table["long"].default_value
        1337

        The default value can also not be changed to ``None``:

        >>> table = session.create_table("Stringly", data_types={"String": "String"})
        >>> table["String"].default_value = None
        Traceback (most recent call last):
            ...
        atoti._graphql_client.exceptions.GraphQLClientGraphQLMultiError: Cannot define a null default value for a non-nullable type.
        >>> table["String"].default_value
        'N/A'
        >>> del session.tables["Stringly"]
        >>> table = session.create_table(
        ...     "Stringly",
        ...     data_types={"String": "String"},
        ...     default_values={"String": None},
        ... )
        >>> print(table["String"].default_value)
        None
        """
        assert self._atoti_client._graphql_client
        table = check_named_object_defined(
            self._atoti_client._graphql_client.get_column_default_value(
                column_name=self.name,
                table_name=self._identifier.table_identifier.table_name,
            ).data_model.table,
            "table",
            self._identifier.table_identifier.table_name,
        )
        default_value = check_named_object_defined(
            table.column,
            "column",
            self.name,
        ).default_value
        return None if default_value is None else default_value.value

    @default_value.setter
    def default_value(self, default_value: ConstantValue | None) -> None:
        assert self._atoti_client._graphql_client
        self._atoti_client._graphql_client.update_column(
            UpdateColumnInput(
                actions=[
                    UpdateColumnAction(
                        set_default_value=SetColumnDefaultValue(
                            value=None
                            if default_value is None
                            else Constant.of(default_value),
                        ),
                    ),
                ],
                column_identifier=self._identifier._graphql_input,
            ),
        )

    @overload
    def isin(
        self,
        *elements: ConstantValue,
    ) -> Condition[ColumnIdentifier, Literal["isin"], Constant, None]: ...

    @overload
    def isin(
        self,
        *elements: ConstantValue | None,
    ) -> Condition[ColumnIdentifier, Literal["isin"], Constant | None, None]: ...

    def isin(
        self,
        *elements: ConstantValue | None,
    ) -> Condition[ColumnIdentifier, Literal["isin"], Constant | None, None]:
        """Return a condition evaluating to ``True`` if a column element is among the given elements and ``False`` otherwise.

        ``table["City"].isin("Paris", "New York")`` is equivalent to ``(table["City"] == "Paris") | (table["City"] == "New York")``.

        Args:
            elements: One or more elements on which the column should be.
        """
        return IsinCondition(
            self._operation_operand,
            {None if element is None else Constant.of(element) for element in elements},
        )

    @override
    def _repr_json_(self) -> ReprJson:
        return {
            "key": self.name in self._table_keys,
            "type": self.data_type,
            "default_value": self.default_value
            if isinstance(self.default_value, type(None) | bool | int | float | str)
            else repr(self.default_value),
        }, {"expanded": True, "root": self.name}
