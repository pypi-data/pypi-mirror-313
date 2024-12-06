from __future__ import annotations

from collections.abc import Iterator, Mapping, MutableMapping
from typing import Final, Literal, final

from pydantic import JsonValue
from typing_extensions import deprecated, override

from ._atoti_client import AtotiClient
from ._check_named_object_defined import check_named_object_defined
from ._constant import Constant, ConstantValue
from ._deprecated_warning_category import (
    DEPRECATED_WARNING_CATEGORY as _DEPRECATED_WARNING_CATEGORY,
)
from ._graphql_client import (
    SetHierarchyAreMembersIndexedByName,
    SetHierarchyIsVisible,
    UpdateHierarchyAction,
    UpdateHierarchyInput,
)
from ._hierarchy_properties import HierarchyProperties
from ._identification import (
    CubeIdentifier,
    DimensionName,
    HasIdentifier,
    HierarchyIdentifier,
    LevelIdentifier,
    LevelName,
    check_not_reserved_dimension_name,
)
from ._ipython import ReprJson, ReprJsonable
from ._java_api import JavaApi
from ._live_extension_unavailable_error import LiveExtensionUnavailableError
from ._operation import Condition, HierarchyIsinCondition
from .level import Level


@final
class Hierarchy(
    Mapping[LevelName, Level],
    HasIdentifier[HierarchyIdentifier],
    ReprJsonable,
):
    """Hierarchy of a :class:`~atoti.Cube`.

    A hierarchy is a sub category of a :attr:`~dimension` and represents a precise type of data.

    For example, :guilabel:`Quarter` or :guilabel:`Week` could be hierarchies in the :guilabel:`Time` dimension.

    See Also:
        :class:`~atoti.hierarchies.Hierarchies` to define one.
    """

    def __init__(
        self,
        identifier: HierarchyIdentifier,
        /,
        *,
        atoti_client: AtotiClient,
        cube_identifier: CubeIdentifier,
        java_api: JavaApi | None,
    ) -> None:
        self._atoti_client: Final = atoti_client
        self._cube_identifier: Final = cube_identifier
        self.__identifier = identifier
        self.__java_api: Final = java_api

    @override
    def __hash__(self) -> int:
        # See comment in `OperandConvertible.__hash__()`.
        return id(self)

    @property
    def dimension(self) -> DimensionName:
        """Name of the dimension of the hierarchy.

        A dimension is a logical group of attributes (e.g. :guilabel:`Geography`).
        It can be thought of as a folder containing hierarchies.

        Note:
            If all the hierarchies in a dimension have their deepest level of type ``TIME``, the dimension's type will be set to ``TIME`` too.
            This can be useful for some clients such as Excel which rely on the dimension's type to be ``TIME`` to decide whether to display date filters.
        """
        return self._identifier.dimension_name

    @dimension.setter
    def dimension(self, value: DimensionName, /) -> None:
        check_not_reserved_dimension_name(value)

        self._java_api.update_hierarchy_dimension(
            self._identifier,
            value,
            cube_name=self._cube_identifier.cube_name,
        )
        self._java_api.refresh()
        self.__identifier = HierarchyIdentifier(value, self.name)

    @property
    def dimension_default(self) -> bool:
        """Whether the hierarchy is the default in its :attr:`~atoti.Hierarchy.dimension` or not.

        Some UIs support clicking on a dimension (or drag and dropping it) as a shortcut to add its default hierarchy to a widget.

        Example:
            .. doctest::
                :hide:

                >>> session = getfixture("default_session")

            >>> table = session.create_table(
            ...     "Sales",
            ...     data_types={
            ...         "Product": "String",
            ...         "Shop": "String",
            ...         "Customer": "String",
            ...         "Date": "LocalDate",
            ...     },
            ... )
            >>> cube = session.create_cube(table, mode="manual")
            >>> h = cube.hierarchies
            >>> for column_name in table:
            ...     h[column_name] = [table[column_name]]
            ...     assert h[column_name].dimension == table.name

            By default, the default hierarchy of a dimension is the first created one:

            >>> h["Product"].dimension_default
            True
            >>> h["Shop"].dimension_default
            False
            >>> h["Customer"].dimension_default
            False
            >>> h["Date"].dimension_default
            False

            There can only be one default hierarchy per dimension:

            >>> h["Shop"].dimension_default = True
            >>> h["Product"].dimension_default
            False
            >>> h["Shop"].dimension_default
            True
            >>> h["Customer"].dimension_default
            False
            >>> h["Date"].dimension_default
            False

            When the default hierarchy is deleted, the first created remaining one becomes the default:

            >>> del h["Shop"]
            >>> h["Product"].dimension_default
            True
            >>> h["Customer"].dimension_default
            False
            >>> h["Date"].dimension_default
            False

            The same thing occurs if the default hierarchy is moved to another dimension:

            >>> h["Product"].dimension = "Product"
            >>> h["Customer"].dimension_default
            True
            >>> h["Date"].dimension_default
            False

            Since :guilabel:`Product` is the first created hierarchy of the newly created dimension, it is the default one there:

            >>> h["Product"].dimension_default
            True

        """
        if not self._atoti_client._graphql_client:
            cube_discovery = self._atoti_client.get_cube_discovery()
            return (
                cube_discovery.cubes[self._cube_identifier.cube_name]
                .name_to_dimension[self.dimension]
                .default_hierarchy
                == self.name
            )

        cube = check_named_object_defined(
            self._atoti_client._graphql_client.get_dimension_default_hierarchy(
                cube_name=self._cube_identifier.cube_name,
                dimension_name=self.dimension,
            ).data_model.cube,
            "cube",
            self._cube_identifier.cube_name,
        )
        dimension = check_named_object_defined(
            cube.dimension,
            "dimension",
            self.dimension,
        )
        return dimension.default_hierarchy.name == self.name

    @dimension_default.setter
    def dimension_default(self, dimension_default: bool, /) -> None:
        self._java_api.set_hierarchy_dimension_default(
            self._identifier,
            dimension_default,
            cube_name=self._cube_identifier.cube_name,
        )
        self._java_api.refresh()
        self._dimension_default = dimension_default

    @property
    @override
    def _identifier(self) -> HierarchyIdentifier:
        return self.__identifier

    def isin(
        self,
        *member_paths: tuple[ConstantValue, ...],
    ) -> Condition[HierarchyIdentifier, Literal["isin"], Constant, None]:
        """Return a condition to check that the hierarchy is on one of the given members.

        Considering ``hierarchy_1`` containing ``level_1`` and ``level_2``, ``hierarchy_1.isin((a,), (b, c))`` is equivalent to ``(level_1 == a) | ((level_1 == b) & (level_2 == c))``.

        Args:
            member_paths: One or more member paths expressed as tuples on which the hierarchy should be.
                Each element in a tuple corresponds to a level of the hierarchy, from the shallowest to the deepest.

        Example:
            .. doctest::
                :hide:

                >>> session = getfixture("default_session")

            >>> df = pd.DataFrame(
            ...     columns=["Country", "City", "Price"],
            ...     data=[
            ...         ("Germany", "Berlin", 150.0),
            ...         ("Germany", "Hamburg", 120.0),
            ...         ("United Kingdom", "London", 240.0),
            ...         ("United States", "New York", 270.0),
            ...         ("France", "Paris", 200.0),
            ...     ],
            ... )
            >>> table = session.read_pandas(
            ...     df, keys={"Country", "City"}, table_name="Example"
            ... )
            >>> cube = session.create_cube(table)
            >>> h, l, m = cube.hierarchies, cube.levels, cube.measures
            >>> h["Geography"] = [l["Country"], l["City"]]
            >>> m["Price.SUM in Germany and Paris"] = tt.filter(
            ...     m["Price.SUM"],
            ...     h["Geography"].isin(("Germany",), ("France", "Paris")),
            ... )
            >>> cube.query(
            ...     m["Price.SUM"],
            ...     m["Price.SUM in Germany and Paris"],
            ...     levels=[l["Geography", "City"]],
            ... )
                                    Price.SUM Price.SUM in Germany and Paris
            Country        City
            France         Paris       200.00                         200.00
            Germany        Berlin      150.00                         150.00
                           Hamburg     120.00                         120.00
            United Kingdom London      240.00
            United States  New York    270.00

        """
        return HierarchyIsinCondition(
            self._identifier,
            {
                tuple(Constant.of(member) for member in member_path)
                for member_path in member_paths
            },
            level_names=list(self),
        )

    @property
    def _java_api(self) -> JavaApi:
        if self.__java_api is None:
            raise LiveExtensionUnavailableError
        return self.__java_api

    def _get_level_names(self, *, key: LevelName | None) -> list[LevelName]:
        # Remove `not self.__java_api` once distributed sessions are supported.
        if not self.__java_api or not self._atoti_client._graphql_client:
            cube_discovery = self._atoti_client.get_cube_discovery()
            hierarchy = (
                cube_discovery.cubes[self._cube_identifier.cube_name]
                .name_to_dimension[self.dimension]
                .name_to_hierarchy[self.name]
            )
            return [
                level.name
                for level in hierarchy.levels
                if level.type != "ALL" and (key is None or level.name == key)
            ]

        if key is None:
            cube = check_named_object_defined(
                self._atoti_client._graphql_client.get_hierarchy_levels(
                    cube_name=self._cube_identifier.cube_name,
                    dimension_name=self.dimension,
                    hierarchy_name=self.name,
                ).data_model.cube,
                "cube",
                self._cube_identifier.cube_name,
            )
            dimension = check_named_object_defined(
                cube.dimension,
                "dimension",
                self.dimension,
            )
            hierarchy = check_named_object_defined(  # type: ignore[assignment]
                dimension.hierarchy,
                "hierarchy",
                self.name,
            )
            return [
                level.name
                for level in hierarchy.levels
                if level.type.value != "ALL"  # type: ignore[attr-defined]
            ]

        cube = check_named_object_defined(  # type: ignore[assignment]
            self._atoti_client._graphql_client.find_level(
                cube_name=self._cube_identifier.cube_name,
                dimension_name=self.dimension,
                hierarchy_name=self.name,
                level_name=key,
            ).data_model.cube,
            "cube",
            self._cube_identifier.cube_name,
        )
        dimension = check_named_object_defined(
            cube.dimension,
            "dimension",
            self.dimension,
        )
        hierarchy = check_named_object_defined(  # type: ignore[assignment]
            dimension.hierarchy,
            "hierarchy",
            self.name,
        )
        return (
            [hierarchy.level.name]  # type: ignore[attr-defined]
            if hierarchy.level and hierarchy.level.type.value != "ALL"  # type: ignore[attr-defined]
            else []
        )

    @property
    @deprecated(
        "`Hierarchy.levels` is deprecated, iterate on the hierarchy instead.",
        category=_DEPRECATED_WARNING_CATEGORY,
    )
    def levels(self) -> Mapping[str, Level]:
        """Levels of the hierarchy.

        :meta private:
        """
        return {
            level_name: Level(
                LevelIdentifier(self._identifier, level_name),
                atoti_client=self._atoti_client,
                cube_identifier=self._cube_identifier,
                java_api=self.__java_api,
            )
            for level_name in self._get_level_names(key=None)
        }

    @override
    def __getitem__(self, key: LevelName, /) -> Level:
        level_names = self._get_level_names(key=key)
        if not level_names:
            raise KeyError(key)
        assert len(level_names) == 1
        return Level(
            LevelIdentifier(self._identifier, level_names[0]),
            atoti_client=self._atoti_client,
            cube_identifier=self._cube_identifier,
            java_api=self.__java_api,
        )

    @override
    def __iter__(self) -> Iterator[LevelName]:
        return iter(self._get_level_names(key=None))

    @override
    def __len__(self) -> int:
        return len(self._get_level_names(key=None))

    @property
    def name(self) -> str:
        """Name of the hierarchy."""
        return self._identifier.hierarchy_name

    @property
    def _properties(self) -> MutableMapping[str, JsonValue]:
        return HierarchyProperties(
            cube_name=self._cube_identifier.cube_name,
            hierarchy_identifier=self._identifier,
            java_api=self._java_api,
        )

    @override
    def _repr_json_(self) -> ReprJson:
        root = f"{self.name}{' (slicing)' if self.slicing else ''}"
        return (
            list(self),
            {
                "root": root,
                "expanded": False,
            },
        )

    @property
    def slicing(self) -> bool:
        """Whether the hierarchy is slicing or not.

        * A regular (i.e. non-slicing) hierarchy is considered aggregable, meaning that it makes sense to aggregate data across all members of the hierarchy.

          For instance, for a :guilabel:`Geography` hierarchy, it is useful to see the worldwide aggregated :guilabel:`Turnover` across all countries.

        * A slicing hierarchy is not aggregable at the top level, meaning that it does not make sense to aggregate data across all members of the hierarchy.

          For instance, for an :guilabel:`As of date` hierarchy giving the current bank account :guilabel:`Balance` for a given date, it does not provide any meaningful information to aggregate the :guilabel:`Balance` across all the dates.
        """
        # Remove `not self.__java_api` once distributed sessions are supported.
        if not self.__java_api or not self._atoti_client._graphql_client:
            cube_discovery = self._atoti_client.get_cube_discovery()
            return (
                cube_discovery.cubes[self._cube_identifier.cube_name]
                .name_to_dimension[self.dimension]
                .name_to_hierarchy[self.name]
                .slicing
            )

        cube = check_named_object_defined(
            self._atoti_client._graphql_client.get_hierarchy_is_slicing(
                cube_name=self._cube_identifier.cube_name,
                dimension_name=self.dimension,
                hierarchy_name=self.name,
            ).data_model.cube,
            "cube",
            self._cube_identifier.cube_name,
        )
        dimension = check_named_object_defined(
            cube.dimension,
            "dimension",
            self.dimension,
        )
        hierarchy = check_named_object_defined(
            dimension.hierarchy,
            "hierarchy",
            self.name,
        )
        return hierarchy.is_slicing

    @slicing.setter
    def slicing(self, value: bool, /) -> None:
        self._java_api.update_hierarchy_slicing(
            self._identifier,
            value,
            cube_name=self._cube_identifier.cube_name,
        )
        self._java_api.refresh()

    @property
    def virtual(self) -> bool | None:
        """Whether the hierarchy is virtual or not.

        A virtual hierarchy is a lightweight hierarchy which does not store in memory the list of its members.
        It is useful for hierarchies with large cardinality.
        """
        # Remove `not self.__java_api` once distributed sessions are supported.
        if not self.__java_api or not self._atoti_client._graphql_client:
            return None

        cube = check_named_object_defined(
            self._atoti_client._graphql_client.get_hierarchy_is_virtual(
                cube_name=self._cube_identifier.cube_name,
                dimension_name=self.dimension,
                hierarchy_name=self.name,
            ).data_model.cube,
            "cube",
            self._cube_identifier.cube_name,
        )
        dimension = check_named_object_defined(
            cube.dimension,
            "dimension",
            self.dimension,
        )
        hierarchy = check_named_object_defined(
            dimension.hierarchy,
            "hierarchy",
            self.name,
        )
        return hierarchy.is_virtual

    @virtual.setter
    def virtual(self, virtual: bool, /) -> None:
        self._java_api.update_hierarchy_virtual(
            self._identifier,
            virtual,
            cube_name=self._cube_identifier.cube_name,
        )
        self._java_api.refresh()

    @property
    def visible(self) -> bool:
        """Whether the hierarchy is visible or not."""
        # Remove `not self.__java_api` once distributed sessions are supported.
        if not self.__java_api or not self._atoti_client._graphql_client:
            cube_discovery = self._atoti_client.get_cube_discovery()
            return (
                cube_discovery.cubes[self._cube_identifier.cube_name]
                .name_to_dimension[self.dimension]
                .name_to_hierarchy[self.name]
                .visible
            )

        cube = check_named_object_defined(
            self._atoti_client._graphql_client.get_hierarchy_is_visible(
                cube_name=self._cube_identifier.cube_name,
                dimension_name=self.dimension,
                hierarchy_name=self.name,
            ).data_model.cube,
            "cube",
            self._cube_identifier.cube_name,
        )
        dimension = check_named_object_defined(
            cube.dimension,
            "dimension",
            self.dimension,
        )
        hierarchy = check_named_object_defined(
            dimension.hierarchy,
            "hierarchy",
            self.name,
        )
        return hierarchy.is_visible

    @visible.setter
    def visible(self, value: bool, /) -> None:
        self._update(
            UpdateHierarchyAction(
                set_is_visible=SetHierarchyIsVisible(value=value),
            ),
        )

    @property
    def members_indexed_by_name(self) -> bool:
        """Whether the hierarchy maintains an index of its members by name.

        :meta private:
        """
        assert self._atoti_client._graphql_client
        cube = check_named_object_defined(
            self._atoti_client._graphql_client.get_hierarchy_are_members_indexed_by_name(
                cube_name=self._cube_identifier.cube_name,
                dimension_name=self.dimension,
                hierarchy_name=self.name,
            ).data_model.cube,
            "cube",
            self._cube_identifier.cube_name,
        )
        dimension = check_named_object_defined(
            cube.dimension,
            "dimension",
            self.dimension,
        )
        hierarchy = check_named_object_defined(
            dimension.hierarchy,
            "hierarchy",
            self.name,
        )
        return hierarchy.are_members_indexed_by_name

    @members_indexed_by_name.setter
    def members_indexed_by_name(self, value: bool, /) -> None:
        self._update(
            UpdateHierarchyAction(
                set_are_members_indexed_by_name=SetHierarchyAreMembersIndexedByName(
                    value=value,
                ),
            ),
        )

    def _update(self, *actions: UpdateHierarchyAction) -> None:
        assert self._atoti_client._graphql_client
        self._atoti_client._graphql_client.update_hierarchy(
            UpdateHierarchyInput(
                actions=list(actions),
                cube_identifier=self._cube_identifier._graphql_input,
                hierarchy_identifier=self._identifier._graphql_input,
            ),
        )
