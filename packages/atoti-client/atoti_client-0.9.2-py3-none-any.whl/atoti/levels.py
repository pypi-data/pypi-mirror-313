from __future__ import annotations

import operator
from collections.abc import Mapping
from typing import Final, final

from typing_extensions import override

from ._atoti_client import AtotiClient
from ._check_named_object_defined import check_named_object_defined
from ._collections import DelegatingKeyDisambiguatingMapping
from ._identification import (
    RESERVED_DIMENSION_NAMES as _RESERVED_DIMENSION_NAMES,
    CubeIdentifier,
    DimensionName,
    HierarchyIdentifier,
    HierarchyName,
    LevelIdentifier,
    LevelKey,
    LevelName,
    LevelUnambiguousKey,
)
from ._ipython import KeyCompletable, ReprJson, ReprJsonable
from ._java_api import JavaApi
from ._live_extension_unavailable_error import LiveExtensionUnavailableError
from .hierarchies import Hierarchies
from .level import Level


def _normalize_key(
    key: LevelKey,
    /,
) -> tuple[DimensionName | None, HierarchyName | None, LevelName]:
    match key:
        case str():
            return None, None, key
        case (hierarchy_name, level_name):
            return None, hierarchy_name, level_name
        case _:
            return key  # type: ignore[return-value]


@final
class Levels(
    DelegatingKeyDisambiguatingMapping[LevelKey, LevelUnambiguousKey, Level],
    KeyCompletable,
    ReprJsonable,
):
    r"""Flat representation of all the :class:`~atoti.Level`\ s in a :class:`~atoti.Cube`."""

    def __init__(
        self,
        *,
        atoti_client: AtotiClient,
        cube_identifier: CubeIdentifier,
        hierarchies: Hierarchies,
        java_api: JavaApi | None,
    ) -> None:
        self._atoti_client: Final = atoti_client
        self._cube_identifier: Final = cube_identifier
        self._hierarchies: Final = hierarchies
        self.__java_api: Final = java_api

    @property
    def _java_api(self) -> JavaApi:
        if self.__java_api is None:
            raise LiveExtensionUnavailableError
        return self.__java_api

    def _get_level_identifiers(self, *, key: LevelKey | None) -> list[LevelIdentifier]:  # noqa: PLR0911
        dimension_name, hierarchy_name, level_name = (
            (None, None, None) if key is None else _normalize_key(key)
        )

        # Remove `not self.__java_api` once distributed sessions are supported.
        if not self.__java_api or not self._atoti_client._graphql_client:
            cube_discovery = self._atoti_client.get_cube_discovery()
            return [
                LevelIdentifier(
                    HierarchyIdentifier(dimension.name, hierarchy.name),
                    level.name,
                )
                for dimension in cube_discovery.cubes[
                    self._cube_identifier.cube_name
                ].dimensions
                if dimension.name not in _RESERVED_DIMENSION_NAMES
                and (dimension_name is None or dimension.name == dimension_name)
                for hierarchy in dimension.hierarchies
                if hierarchy_name is None or hierarchy.name == hierarchy_name
                for level in hierarchy.levels
                if (level.type != "ALL")
                and (level_name is None or level.name == level_name)
            ]

        if level_name is None:
            cube = check_named_object_defined(
                self._atoti_client._graphql_client.get_levels(
                    cube_name=self._cube_identifier.cube_name,
                ).data_model.cube,
                "cube",
                self._cube_identifier.cube_name,
            )
            return [
                LevelIdentifier(
                    HierarchyIdentifier(dimension.name, hierarchy.name),
                    level.name,
                )
                for dimension in cube.dimensions
                if dimension.name not in _RESERVED_DIMENSION_NAMES
                for hierarchy in dimension.hierarchies
                for level in hierarchy.levels
                if level.type.value != "ALL"
            ]

        if hierarchy_name is None:
            cube = check_named_object_defined(  # type: ignore[assignment]
                self._atoti_client._graphql_client.find_level_across_hierarchies(
                    cube_name=self._cube_identifier.cube_name,
                    level_name=level_name,
                ).data_model.cube,
                "cube",
                self._cube_identifier.cube_name,
            )
            return [
                LevelIdentifier(
                    HierarchyIdentifier(dimension.name, hierarchy.name),
                    hierarchy.level.name,  # type: ignore[attr-defined]
                )
                for dimension in cube.dimensions
                if dimension.name not in _RESERVED_DIMENSION_NAMES
                for hierarchy in dimension.hierarchies
                if hierarchy.level and hierarchy.level.type.value != "ALL"  # type: ignore[attr-defined]
            ]

        if dimension_name is None:
            cube = check_named_object_defined(  # type: ignore[assignment]
                self._atoti_client._graphql_client.find_level_across_dimensions(
                    cube_name=self._cube_identifier.cube_name,
                    hierarchy_name=hierarchy_name,
                    level_name=level_name,
                ).data_model.cube,
                "cube",
                self._cube_identifier.cube_name,
            )
            return [
                LevelIdentifier(
                    HierarchyIdentifier(dimension.name, dimension.hierarchy.name),  # type: ignore[attr-defined]
                    dimension.hierarchy.level.name,  # type: ignore[attr-defined]
                )
                for dimension in cube.dimensions
                if dimension.name not in _RESERVED_DIMENSION_NAMES
                and dimension.hierarchy  # type: ignore[attr-defined]
                and dimension.hierarchy.level  # type: ignore[attr-defined]
                and dimension.hierarchy.level.type.value != "ALL"  # type: ignore[attr-defined]
            ]

        cube = check_named_object_defined(  # type: ignore[assignment]
            self._atoti_client._graphql_client.find_level(
                cube_name=self._cube_identifier.cube_name,
                dimension_name=dimension_name,
                hierarchy_name=hierarchy_name,
                level_name=level_name,
            ).data_model.cube,
            "cube",
            self._cube_identifier.cube_name,
        )
        dimension = check_named_object_defined(  # type: ignore[var-annotated]
            cube.dimension,  # type: ignore[attr-defined]
            "dimension",
            dimension_name,
            error_kind="key",
        )

        if dimension.name in _RESERVED_DIMENSION_NAMES:
            return []

        hierarchy = check_named_object_defined(  # type: ignore[var-annotated]
            dimension.hierarchy,
            "hierarchy",
            hierarchy_name,
            error_kind="key",
        )
        level = check_named_object_defined(
            hierarchy.level,  # type: ignore[var-annotated]
            "level",
            level_name,
            error_kind="key",
        )

        if level.type.value == "ALL":
            return []

        return [
            LevelIdentifier(
                HierarchyIdentifier(dimension.name, hierarchy.name),
                level.name,
            ),
        ]

    @override
    def _get_delegate(
        self,
        *,
        key: LevelKey | None,
    ) -> Mapping[LevelUnambiguousKey, Level]:
        return {
            identifier.key: Level(
                identifier,
                atoti_client=self._atoti_client,
                cube_identifier=self._cube_identifier,
                java_api=self.__java_api,
            )
            for identifier in self._get_level_identifiers(key=key)
        }

    @override
    def _repr_json_(self) -> ReprJson:
        # Use the dimension/hierarchy/level in the map key to make it unique.
        data = {
            f"{level.name} ({level.dimension}/{level.hierarchy})": level._repr_json_()[
                0
            ]
            for hierarchy in self._hierarchies.values()
            for level in hierarchy.values()
        }
        sorted_data = dict(sorted(data.items(), key=operator.itemgetter(0)))
        return (
            sorted_data,
            {
                "expanded": True,
                "root": "Levels",
            },
        )

    def __delitem__(self, key: LevelKey, /) -> None:
        # Same signature as `MutableMapping.__delitem__()`.
        level = self[key]
        level._java_api.delete_level(
            level._identifier,
            cube_name=self._cube_identifier.cube_name,
        )
        level._java_api.refresh()
