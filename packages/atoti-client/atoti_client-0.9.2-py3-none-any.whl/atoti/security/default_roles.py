from collections.abc import Set as AbstractSet
from typing import Final, final

from typing_extensions import override

from .._collections import DelegatingMutableSet
from ._authentication_type import AuthenticationType
from ._service import Service


@final
class DefaultRoles(DelegatingMutableSet[str]):
    """Roles granted to users who have been granted no :attr:`individual <atoti.security.Security.individual_roles>` and :class:`mapped <atoti.security.role_mapping.RoleMapping>` roles."""

    def __init__(
        self,
        *,
        authentication_type: AuthenticationType,
        service: Service,
    ) -> None:
        self._authentication_type: Final = authentication_type
        self._service: Final = service

    @override
    def _get_delegate(self) -> AbstractSet[str]:
        return self._service.get_default_roles(
            authentication_type=self._authentication_type,
        )

    @override
    def _set_delegate(self, new_set: AbstractSet[str], /) -> None:
        self._service.set_default_roles(
            new_set,
            authentication_type=self._authentication_type,
        )
