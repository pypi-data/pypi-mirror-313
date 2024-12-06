from __future__ import annotations

from collections.abc import Mapping, Set as AbstractSet
from typing import Final, final

from typing_extensions import override

from ._collections import DelegatingMutableMapping
from ._ipython import ReprJson, ReprJsonable
from ._java_api import JavaApi


@final
class SharedContext(DelegatingMutableMapping[str, str], ReprJsonable):  # type: ignore[misc]
    def __init__(self, *, cube_name: str, java_api: JavaApi) -> None:
        self._cube_name: Final = cube_name
        self._java_api: Final = java_api

    @override
    def _get_delegate(self, *, key: str | None) -> Mapping[str, str]:
        return self._java_api.get_shared_context_values(
            cube_name=self._cube_name,
            key=key,
        )

    @override
    def _update_delegate(self, other: Mapping[str, str], /) -> None:
        for key, value in other.items():
            self._java_api.set_shared_context_value(
                key,
                str(value),
                cube_name=self._cube_name,
            )
        self._java_api.refresh()

    @override
    def _delete_delegate_keys(self, keys: AbstractSet[str], /) -> None:
        raise NotImplementedError("Cannot delete context value.")

    @override
    def _repr_json_(self) -> ReprJson:
        return (
            dict(self),
            {"expanded": True, "root": "Context Values"},
        )
