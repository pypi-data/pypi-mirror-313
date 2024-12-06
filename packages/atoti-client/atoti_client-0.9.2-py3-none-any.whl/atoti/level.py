from __future__ import annotations

from collections.abc import MutableMapping
from typing import Final, Literal, final

from typing_extensions import override

from ._atoti_client import AtotiClient
from ._constant import Constant, ConstantValue
from ._data_type import DataType
from ._identification import ColumnIdentifier, Identifiable, LevelIdentifier
from ._identification.cube_identifier import CubeIdentifier
from ._ipython import ReprJson, ReprJsonable
from ._java_api import JavaApi
from ._live_extension_unavailable_error import LiveExtensionUnavailableError
from ._member_properties import MemberProperties
from ._operation import (
    ComparisonCondition,
    Condition,
    IsinCondition,
    OperandConvertibleWithIdentifier,
)
from .order._order import Order


@final
class Level(OperandConvertibleWithIdentifier[LevelIdentifier], ReprJsonable):
    """Level of a :class:`~atoti.Hierarchy`.

    A level is a sub category of a hierarchy.
    Levels have a specific order with a parent-child relationship.

    In a :guilabel:`Pivot Table`, a single-level hierarchy will be displayed as a flat attribute while a multi-level hierarchy will display the first level and allow users to expand each member against the next level and display sub totals.

    For example, a :guilabel:`Geography` hierarchy can have a :guilabel:`Continent` as the top level where :guilabel:`Continent` expands to :guilabel:`Country` which in turn expands to the leaf level: :guilabel:`City`.
    """

    def __init__(
        self,
        identifier: LevelIdentifier,
        /,
        *,
        atoti_client: AtotiClient,
        cube_identifier: CubeIdentifier,
        java_api: JavaApi | None,
    ) -> None:
        self._atoti_client: Final = atoti_client
        self._cube_identifier: Final = cube_identifier
        self.__identifier: Final = identifier
        self.__java_api: Final = java_api

    @property
    def _column_identifier(self) -> ColumnIdentifier | None:
        if not self.__java_api:
            return None

        return self._java_api.get_level_column_identifier(
            self._identifier,
            cube_name=self._cube_identifier.cube_name,
        )

    @property
    def data_type(self) -> DataType:
        """Type of the level members."""
        if not self.__java_api:
            return "Object"

        return self._java_api.get_level_data_type(
            self._identifier,
            cube_name=self._cube_identifier.cube_name,
        )

    @property
    def dimension(self) -> str:
        """Name of the dimension holding the level."""
        return self._identifier.hierarchy_identifier.dimension_name

    @property
    def hierarchy(self) -> str:
        """Name of the hierarchy holding the level."""
        return self._identifier.hierarchy_identifier.hierarchy_name

    @property
    @override
    def _identifier(self) -> LevelIdentifier:
        return self.__identifier

    def isin(
        self,
        *members: ConstantValue,
    ) -> Condition[LevelIdentifier, Literal["isin"], Constant, None]:
        """Return a condition to check that the level is on one of the given members.

        ``level.isin(a, b)`` is equivalent to ``(level == a) | (level == b)``.

        Args:
            members: One or more members on which the level should be.

        Example:
            .. doctest::
                :hide:

                >>> session = getfixture("default_session")

            >>> df = pd.DataFrame(
            ...     columns=["City", "Price"],
            ...     data=[
            ...         ("Berlin", 150.0),
            ...         ("London", 240.0),
            ...         ("New York", 270.0),
            ...         ("Paris", 200.0),
            ...     ],
            ... )
            >>> table = session.read_pandas(df, keys={"City"}, table_name="Example")
            >>> cube = session.create_cube(table)
            >>> l, m = cube.levels, cube.measures
            >>> m["Price.SUM in London and Paris"] = tt.filter(
            ...     m["Price.SUM"], l["City"].isin("London", "Paris")
            ... )
            >>> cube.query(
            ...     m["Price.SUM"],
            ...     m["Price.SUM in London and Paris"],
            ...     levels=[l["City"]],
            ... )
                     Price.SUM Price.SUM in London and Paris
            City
            Berlin      150.00
            London      240.00                        240.00
            New York    270.00
            Paris       200.00                        200.00

        """
        return IsinCondition(
            self._operation_operand,
            {Constant.of(member) for member in members},
        )

    @override
    def isnull(
        self,
    ) -> Condition[LevelIdentifier, Literal["eq"], None, None]:
        """Return a condition evaluating to ``True`` when a level is not expressed in a query and ``False`` otherwise.

        Use `~level.isnull()` for the opposite behavior.

        Example:
            .. doctest::
                :hide:

                >>> session = getfixture("default_session")

            >>> df = pd.DataFrame(
            ...     columns=["Country", "City", "Price"],
            ...     data=[
            ...         ("France", "Paris", 200.0),
            ...         ("Germany", "Berlin", 120),
            ...     ],
            ... )
            >>> table = session.read_pandas(df, table_name="Example")
            >>> cube = session.create_cube(table)
            >>> l, m = cube.levels, cube.measures
            >>> m["City.isnull"] = l["City"].isnull()
            >>> m["City.notnull"] = ~l["City"].isnull()
            >>> cube.query(
            ...     m["City.isnull"],
            ...     m["City.notnull"],
            ...     levels=[l["Country"], l["City"]],
            ...     include_totals=True,
            ... )
                           City.isnull City.notnull
            Country City
            Total                 True        False
            France                True        False
                    Paris        False         True
            Germany               True        False
                    Berlin       False         True

        """
        return ComparisonCondition(self._operation_operand, "eq", None)

    @property
    def _java_api(self) -> JavaApi:
        if self.__java_api is None:
            raise LiveExtensionUnavailableError
        return self.__java_api

    @property
    def _member_properties(self) -> MutableMapping[str, Identifiable[ColumnIdentifier]]:
        """The custom properties of the members of this level.

        Member properties allow to attach some attributes to a member without creating dedicated levels.
        The properties can be requested in MDX queries.

        The keys in the mapping are the names of the custom properties.
        The values are table columns from which property values will be read.
        These columns can come from different tables.
        These tables do not have to be joined but they must have either:

        * a single key column
        * as many key columns as the number of levels of this level's hierarchy (not implemented yet)

        These keys columns will be used to determine which table row corresponds to which level member.
        If a member does not have a corresponding table row, the property value will be ``None``.

        Note:
            Members have intrinsic properties such as :guilabel:`CAPTION`, :guilabel:`DESCRIPTION`, or :guilabel:`MEMBER_TYPE`.
            These properties cannot be overridden through this mapping.

        Example:
            .. doctest::
                :hide:

                >>> session = getfixture("default_session")

            >>> populations_df = pd.DataFrame(
            ...     columns=["City", "Population"],
            ...     data=[
            ...         ("New York City", 8468000),
            ...         ("Las Vegas", 646790),
            ...         ("New Orleans", 376971),
            ...     ],
            ... )
            >>> populations_table = session.read_pandas(
            ...     populations_df, keys={"City"}, table_name="Populations"
            ... )
            >>> nicknames_df = pd.DataFrame(
            ...     columns=["City name", "First", "Second"],
            ...     data=[
            ...         ("New York City", "The Big Apple", "Gotham"),
            ...         ("Las Vegas", "Sin City", "What Happens Here, Stays Here"),
            ...         ("New Orleans", "The Big Easy", None),
            ...     ],
            ... )
            >>> nicknames_table = session.read_pandas(
            ...     nicknames_df,
            ...     default_values={"Second": None},
            ...     keys={"City name"},
            ...     table_name="Nicknames",
            ... )
            >>> climates_df = pd.DataFrame(
            ...     columns=["Name", "Climate"],
            ...     data=[
            ...         ("Las Vegas", "subtropical hot desert climate"),
            ...         ("New Orleans", "humid subtropical"),
            ...     ],
            ... )
            >>> climates_table = session.read_pandas(
            ...     climates_df, keys={"Name"}, table_name="Climates"
            ... )
            >>> cube = session.create_cube(populations_table)
            >>> l, m = cube.levels, cube.measures
            >>> l["City"]._member_properties
            {}
            >>> l["City"]._member_properties.update(
            ...     {
            ...         "FIRST_ALIAS": nicknames_table["First"],
            ...         "SECOND_ALIAS": nicknames_table["Second"],
            ...         "CLIMATE": climates_table["Climate"],
            ...     }
            ... )
            >>> mdx = (
            ...     " WITH"
            ...     "   Member [Measures].[First alias]"
            ...     "     AS [Populations].[City].CurrentMember.Properties('FIRST_ALIAS')"
            ...     "   Member [Measures].[Second alias]"
            ...     "     AS [Populations].[City].CurrentMember.Properties('SECOND_ALIAS')"
            ...     "   Member [Measures].[Climate]"
            ...     "     AS [Populations].[City].CurrentMember.Properties('CLIMATE')"
            ...     " SELECT"
            ...     "   [Populations].[City].Members ON ROWS,"
            ...     "   {"
            ...     "     [Measures].[Population.SUM],"
            ...     "     [Measures].[First alias],"
            ...     "     [Measures].[Second alias],"
            ...     "     [Measures].[Climate]"
            ...     "   } ON COLUMNS"
            ...     "   FROM [Populations]"
            ... )
            >>> session.query_mdx(mdx)
                          Population.SUM    First alias                   Second alias                         Climate
            City
            Las Vegas            646,790       Sin City  What Happens Here, Stays Here  subtropical hot desert climate
            New Orleans          376,971   The Big Easy                                              humid subtropical
            New York City      8,468,000  The Big Apple                         Gotham

        """
        return MemberProperties(
            cube_name=self._cube_identifier.cube_name,
            level_identifier=self._identifier,
            java_api=self._java_api,
        )

    @property
    def name(self) -> str:
        """Name of the level."""
        return self._identifier.level_name

    @property
    @override
    def _operation_operand(self) -> LevelIdentifier:
        return self._identifier

    @property
    def order(self) -> Order:
        """Order in which to sort the level's members.

        Defaults to ascending :class:`atoti.NaturalOrder`.
        """
        return self._java_api.get_level_order(
            self._identifier,
            cube_name=self._cube_identifier.cube_name,
        )

    @order.setter
    def order(self, value: Order) -> None:
        self._java_api.update_level_order(
            self._identifier,
            value,
            cube_name=self._cube_identifier.cube_name,
        )
        self._java_api.refresh()

    @override
    def _repr_json_(self) -> ReprJson:
        data = {
            "dimension": self.dimension,
            "hierarchy": self.hierarchy,
            "data type": str(self.data_type),
        }

        if self.__java_api:
            data["order"] = self.order._key

        return data, {"expanded": True, "root": self.name}
