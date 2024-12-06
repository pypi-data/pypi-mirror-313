from __future__ import annotations

from collections.abc import Mapping, Set as AbstractSet
from typing import Final, final

from typing_extensions import override

from .._collections import DelegatingMutableMapping
from ._constants import SPECIAL_ROLES
from ._restriction import Restriction
from ._service import Service


@final
class Restrictions(DelegatingMutableMapping[str, Restriction]):
    def __init__(self, *, service: Service) -> None:
        self._service: Final = service

    @override
    def _get_delegate(self, *, key: str | None) -> Mapping[str, Restriction]:
        return {
            role_name: restriction
            for role_name, restriction in self._service.restrictions.items()
            if key is None or role_name == key
        }

    @override
    def _update_delegate(self, other: Mapping[str, Restriction], /) -> None:
        for role_name, restriction in other.items():
            if role_name in SPECIAL_ROLES:
                raise ValueError(
                    f"Role `{role_name}` is reserved and cannot be assigned restrictions, use another role.",
                )

            self._service.upsert_restriction(restriction, role_name=role_name)

    @override
    def _delete_delegate_keys(self, keys: AbstractSet[str], /) -> None:
        for role_name in keys:
            self._service.delete_restriction(role_name)
