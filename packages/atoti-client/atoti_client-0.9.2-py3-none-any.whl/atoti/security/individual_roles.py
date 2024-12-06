from __future__ import annotations

from collections.abc import Mapping, Set as AbstractSet
from typing import Final, final

from typing_extensions import override

from .._collections import DelegatingMutableMapping
from ._service import Service


@final
class IndividualRoles(DelegatingMutableMapping[str, AbstractSet[str]]):
    """Mapping from username to roles granted on top of the ones that can be added by authentication providers.

    Example:
        >>> session_config = tt.SessionConfig(security=tt.SecurityConfig())
        >>> session = tt.Session.start(session_config)
        >>> username = "John"
        >>> session.security.basic_authentication.credentials[username] = "X Æ A-12"
        >>> username in session.security.individual_roles
        False
        >>> session.security.individual_roles[username] = {
        ...     "ROLE_USA",
        ...     "ROLE_USER",
        ... }
        >>> sorted(session.security.individual_roles[username])
        ['ROLE_USA', 'ROLE_USER']
        >>> session.security.individual_roles[username] -= {"ROLE_USA"}
        >>> session.security.individual_roles[username]
        frozenset({'ROLE_USER'})
        >>> # Removing all the roles will prevent the user from accessing the application:
        >>> del session.security.individual_roles[username]
        >>> username in session.security.individual_roles
        False

        .. doctest::
            :hide:

            >>> del session

    """

    def __init__(self, *, service: Service) -> None:
        self._service: Final = service

    @override
    def _get_delegate(self, *, key: str | None) -> Mapping[str, AbstractSet[str]]:
        return {
            username: frozenset(roles)
            for username, roles in self._service.individual_roles.items()
            if key is None or username == key
        }

    @override
    def _update_delegate(self, other: Mapping[str, AbstractSet[str]], /) -> None:
        for username, roles in other.items():
            self._service.upsert_individual_roles(username, roles=roles)

    @override
    def _delete_delegate_keys(self, keys: AbstractSet[str], /) -> None:
        for username in keys:
            self._service.delete_individual_roles_for_user(username)
