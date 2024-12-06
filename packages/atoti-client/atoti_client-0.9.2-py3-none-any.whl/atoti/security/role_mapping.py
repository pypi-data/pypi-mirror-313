from __future__ import annotations

from collections.abc import Collection, Mapping, Set as AbstractSet
from typing import Final, final

from typing_extensions import override

from .._collections import DelegatingMutableMapping
from ._authentication_type import AuthenticationType
from ._service import Service


@final
class RoleMapping(DelegatingMutableMapping[str, AbstractSet[str]]):
    """Mapping from role or username coming from the authentication provider to roles to use in the session."""

    def __init__(
        self,
        *,
        authentication_type: AuthenticationType,
        service: Service,
    ) -> None:
        self._authentication_type: Final = authentication_type
        self._service: Final = service

    @override
    def _get_delegate(self, *, key: str | None) -> Mapping[str, AbstractSet[str]]:
        role_mapping: Mapping[str, Collection[str]] = self._service.get_role_mapping(
            authentication_type=self._authentication_type,
        )
        return {
            role_name: frozenset(authorities)
            for role_name, authorities in role_mapping.items()
            if key is None or role_name == key
        }

    @override
    def _update_delegate(self, other: Mapping[str, AbstractSet[str]], /) -> None:
        for role_name, authorities in other.items():
            self._service.upsert_role_mapping(
                role_name,
                authentication_type=self._authentication_type,
                authorities=authorities,
            )

    @override
    def _delete_delegate_keys(self, keys: AbstractSet[str], /) -> None:
        for key in keys:
            self._service.remove_role_from_role_mapping(
                key,
                authentication_type=self._authentication_type,
            )
