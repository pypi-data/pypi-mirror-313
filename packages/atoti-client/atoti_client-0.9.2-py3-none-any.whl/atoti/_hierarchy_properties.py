from collections.abc import Mapping, Set as AbstractSet
from typing import Final, final

from pydantic import JsonValue
from typing_extensions import override

from ._collections import DelegatingMutableMapping
from ._identification import HierarchyIdentifier
from ._java_api import JavaApi


@final
class HierarchyProperties(DelegatingMutableMapping[str, JsonValue]):
    def __init__(
        self,
        *,
        cube_name: str,
        hierarchy_identifier: HierarchyIdentifier,
        java_api: JavaApi,
    ):
        self._cube_name: Final = cube_name
        self._hierarchy_identifier: Final = hierarchy_identifier
        self._java_api: Final = java_api

    @override
    def _get_delegate(self, *, key: str | None) -> Mapping[str, JsonValue]:
        return self._java_api.get_hierarchy_properties(
            self._hierarchy_identifier,
            cube_name=self._cube_name,
            key=key,
        )

    @override
    def _update_delegate(self, other: Mapping[str, JsonValue], /) -> None:
        new_value = {**self, **other}
        self._java_api.set_hierarchy_properties(
            self._hierarchy_identifier,
            new_value,
            cube_name=self._cube_name,
        )
        self._java_api.refresh()

    @override
    def _delete_delegate_keys(self, keys: AbstractSet[str], /) -> None:
        new_value = {**self}
        for key in keys or list(new_value):
            del new_value[key]

        self._java_api.set_hierarchy_properties(
            self._hierarchy_identifier,
            new_value,
            cube_name=self._cube_name,
        )
        self._java_api.refresh()
