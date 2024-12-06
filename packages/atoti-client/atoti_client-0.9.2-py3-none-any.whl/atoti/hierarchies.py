from __future__ import annotations

from collections import defaultdict
from collections.abc import Mapping, Sequence, Set as AbstractSet
from typing import Final, final

from typing_extensions import override

from ._atoti_client import AtotiClient
from ._check_named_object_defined import check_named_object_defined
from ._collections import DelegatingConvertingMapping
from ._identification import (
    RESERVED_DIMENSION_NAMES as _RESERVED_DIMENSION_NAMES,
    ColumnIdentifier,
    CubeIdentifier,
    DimensionName,
    HierarchyIdentifier,
    HierarchyKey,
    HierarchyName,
    HierarchyUnambiguousKey,
    LevelName,
)
from ._ipython import ReprJson, ReprJsonable
from ._java_api import JavaApi
from ._live_extension_unavailable_error import LiveExtensionUnavailableError
from .column import Column
from .hierarchy import Hierarchy
from .level import Level


def _infer_dimension_name_from_level_or_column(
    levels_or_column: Level | Column,
) -> str:
    if isinstance(levels_or_column, Level):
        return levels_or_column.dimension
    return levels_or_column._identifier.table_identifier.table_name


def _normalize_key(key: HierarchyKey, /) -> tuple[DimensionName | None, HierarchyName]:
    return (None, key) if isinstance(key, str) else key


_HierarchyConvertible = Sequence[Level | Column] | Mapping[LevelName, Level | Column]


@final
class Hierarchies(
    DelegatingConvertingMapping[
        HierarchyKey,
        HierarchyUnambiguousKey,
        Hierarchy,
        _HierarchyConvertible,
    ],
    ReprJsonable,
):
    """Manage the hierarchies of a :class:`~atoti.Cube`.

    Example:
        .. doctest::
            :hide:

            >>> session = getfixture("default_session")

        >>> prices_df = pd.DataFrame(
        ...     columns=["Nation", "City", "Color", "Price"],
        ...     data=[
        ...         ("France", "Paris", "red", 20.0),
        ...         ("France", "Lyon", "blue", 15.0),
        ...         ("France", "Toulouse", "green", 10.0),
        ...         ("UK", "London", "red", 20.0),
        ...         ("UK", "Manchester", "blue", 15.0),
        ...     ],
        ... )
        >>> table = session.read_pandas(prices_df, table_name="Prices")
        >>> cube = session.create_cube(table, mode="manual")
        >>> h = cube.hierarchies
        >>> h["Nation"] = {"Nation": table["Nation"]}
        >>> list(h)
        [('Prices', 'Nation')]

        A hierarchy can be renamed by copying it and deleting the old one:

        >>> h["Country"] = h["Nation"]
        >>> del h["Nation"]
        >>> list(h)
        [('Prices', 'Country')]
        >>> list(h["Country"])
        ['Nation']

        :meth:`~dict.update` can be used to batch hierarchy creation operations for improved performance:

        >>> h.update(
        ...     {
        ...         ("Geography", "Geography"): [table["Nation"], table["City"]],
        ...         "Color": {"Color": table["Color"]},
        ...     }
        ... )
        >>> sorted(h)
        [('Geography', 'Geography'), ('Prices', 'Color'), ('Prices', 'Country')]

    See Also:
        :class:`~atoti.Hierarchy` to configure existing hierarchies.
    """

    def __init__(
        self,
        *,
        atoti_client: AtotiClient,
        cube_identifier: CubeIdentifier,
        java_api: JavaApi | None,
    ) -> None:
        self._atoti_client: Final = atoti_client
        self._cube_identifier: Final = cube_identifier
        self.__java_api: Final = java_api

    @property
    def _java_api(self) -> JavaApi:
        if self.__java_api is None:
            raise LiveExtensionUnavailableError
        return self.__java_api

    def _get_hierarchy_identifiers(
        self,
        *,
        key: HierarchyKey | None,
    ) -> list[HierarchyIdentifier]:
        dimension_name, hierarchy_name = (
            (None, None) if key is None else _normalize_key(key)
        )

        # Remove `not self.__java_api` once distributed sessions are supported.
        if not self.__java_api or not self._atoti_client._graphql_client:
            cube_discovery = self._atoti_client.get_cube_discovery()
            return [
                HierarchyIdentifier(dimension.name, hierarchy.name)
                for dimension in cube_discovery.cubes[
                    self._cube_identifier.cube_name
                ].dimensions
                if dimension.name not in _RESERVED_DIMENSION_NAMES
                and (dimension_name is None or dimension.name == dimension_name)
                for hierarchy in dimension.hierarchies
                if hierarchy_name is None or hierarchy.name == hierarchy_name
            ]

        if hierarchy_name is None:
            cube = check_named_object_defined(
                self._atoti_client._graphql_client.get_hierarchies(
                    cube_name=self._cube_identifier.cube_name,
                ).data_model.cube,
                "cube",
                self._cube_identifier.cube_name,
            )
            return [
                HierarchyIdentifier(dimension.name, hierarchy.name)
                for dimension in cube.dimensions
                if dimension.name not in _RESERVED_DIMENSION_NAMES
                for hierarchy in dimension.hierarchies
            ]

        if dimension_name is None:
            cube = check_named_object_defined(  # type: ignore[assignment]
                (
                    self._atoti_client._graphql_client.find_hierarchy_across_dimensions(
                        cube_name=self._cube_identifier.cube_name,
                        hierarchy_name=hierarchy_name,
                    )
                ).data_model.cube,
                "cube",
                self._cube_identifier.cube_name,
            )
            return [
                HierarchyIdentifier(dimension.name, dimension.hierarchy.name)  # type: ignore[attr-defined]
                for dimension in cube.dimensions
                if dimension.name not in _RESERVED_DIMENSION_NAMES
                and dimension.hierarchy  # type: ignore[attr-defined]
            ]

        cube = check_named_object_defined(  # type: ignore[assignment]
            (
                self._atoti_client._graphql_client.find_hierarchy(
                    cube_name=self._cube_identifier.cube_name,
                    dimension_name=dimension_name,
                    hierarchy_name=hierarchy_name,
                )
            ).data_model.cube,
            "cube",
            self._cube_identifier.cube_name,
        )
        return (
            [HierarchyIdentifier(cube.dimension.name, cube.dimension.hierarchy.name)]  # type: ignore[attr-defined]
            if cube.dimension  # type: ignore[attr-defined]
            and cube.dimension.name not in _RESERVED_DIMENSION_NAMES  # type: ignore[attr-defined]
            and cube.dimension.hierarchy  # type: ignore[attr-defined]
            else []
        )

    @override
    def _get_delegate(
        self,
        *,
        key: HierarchyKey | None,
    ) -> Mapping[HierarchyUnambiguousKey, Hierarchy]:
        return {
            identifier.key: Hierarchy(
                identifier,
                atoti_client=self._atoti_client,
                cube_identifier=self._cube_identifier,
                java_api=self.__java_api,
            )
            for identifier in self._get_hierarchy_identifiers(key=key)
        }

    @override
    def _update_delegate(
        self,
        other: Mapping[
            HierarchyKey,
            # `None` means delete the hierarchy at this key.
            _HierarchyConvertible | None,
        ],
        /,
    ) -> None:
        deleted: dict[DimensionName, set[HierarchyName]] = defaultdict(set)
        updated: dict[
            DimensionName,
            dict[HierarchyName, Mapping[LevelName, ColumnIdentifier]],
        ] = defaultdict(
            dict,
        )

        for hierarchy_key, levels_or_columns in other.items():
            dimension_name, hierarchy_name = _normalize_key(hierarchy_key)

            if levels_or_columns is not None:
                normalized_levels_or_columns = (
                    levels_or_columns
                    if isinstance(levels_or_columns, Mapping)
                    else {
                        level_or_column.name: level_or_column
                        for level_or_column in levels_or_columns
                    }
                )
                if dimension_name is None:
                    # Check that the hierarchy name is unique across dimensions.
                    assert (hierarchy_name in self) is not None
                    dimension_name = _infer_dimension_name_from_level_or_column(
                        next(iter(normalized_levels_or_columns.values())),
                    )

                column_identifiers: dict[LevelName, ColumnIdentifier] = {}

                for name, level_or_column in normalized_levels_or_columns.items():
                    if isinstance(level_or_column, Column):
                        column_identifiers[name] = level_or_column._identifier
                    else:
                        assert level_or_column._column_identifier is not None
                        column_identifiers[name] = level_or_column._column_identifier

                updated[dimension_name][hierarchy_name] = column_identifiers

            else:
                if dimension_name is None:
                    dimension_name = self[hierarchy_name].dimension

                deleted[dimension_name].add(hierarchy_name)

        self._java_api.update_hierarchies_for_cube(
            self._cube_identifier.cube_name,
            deleted=deleted,
            updated=updated,
        )
        self._java_api.refresh()

    @override
    def _delete_delegate_keys(self, keys: AbstractSet[HierarchyKey], /) -> None:
        for key in keys:
            self._java_api.delete_hierarchy(
                self[key]._identifier,
                cube_name=self._cube_identifier.cube_name,
            )

        # The implementation above should be replaced with the one below but it breaks some tests.
        # deleted: dict[str, set[str]] = defaultdict(set)
        # for key in keys or self.keys():
        #     hierarchy = self[key]
        #     deleted[hierarchy.dimension].add(hierarchy.name)
        # self._java_api.update_hierarchies_for_cube(
        #     self._cube_identifier.cube_name,
        #     deleted=deleted,
        #     updated={},
        # )
        # self._java_api.refresh()

    @override
    def _repr_json_(self) -> ReprJson:
        dimensions: dict[DimensionName, list[Hierarchy]] = defaultdict(list)
        for hierarchy in self.values():
            dimensions[hierarchy.dimension].append(hierarchy)
        json = {
            dimension: dict(
                sorted(
                    {
                        hierarchy._repr_json_()[1]["root"]: hierarchy._repr_json_()[0]
                        for hierarchy in dimension_hierarchies
                    }.items(),
                ),
            )
            for dimension, dimension_hierarchies in sorted(dimensions.items())
        }
        return json, {"expanded": True, "root": "Dimensions"}
