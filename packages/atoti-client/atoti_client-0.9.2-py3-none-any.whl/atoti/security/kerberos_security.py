from typing import Final, final

from ._service import Service
from .default_roles import DefaultRoles


@final
class KerberosSecurity:
    """Manage Kerberos security on the session.

    Note:
        This requires :attr:`atoti.SecurityConfig.sso` to be an instance of :class:`~atoti.KerberosConfig`.

    See Also:
        :attr:`~atoti.security.Security.ldap` for a similar usage example.
    """

    def __init__(self, *, default_roles: DefaultRoles, service: Service) -> None:
        self._default_roles: Final = default_roles
        self._service: Final = service

    @property
    def default_roles(self) -> DefaultRoles:
        return self._default_roles
