from __future__ import annotations

from collections.abc import MutableMapping
from typing import Final, final

from ._service import Service


@final
class BasicAuthenticationSecurity:
    """Manage basic authentication security on the session.

    Note:
        This requires :attr:`atoti.SessionConfig.security` to not be ``None``.
    """

    def __init__(
        self,
        *,
        credentials: MutableMapping[str, str] | None = None,
        service: Service,
    ) -> None:
        self._credentials: Final = credentials
        self._service: Final = service

    @property
    def credentials(self) -> MutableMapping[str, str]:
        """Mapping from username to password.

        Note:
            At the moment, unlike the rest of the :class:`~atoti.security.Security` config, these credentials are transient (kept in memory).
            They are not stored in the :attr:`~atoti.SessionConfig.user_content_storage` and thus will reset when the session stops.

        Use :attr:`~atoti.security.Security.individual_roles` to grant roles to the user.

        Example:
            >>> session_config = tt.SessionConfig(security=tt.SecurityConfig())
            >>> session = tt.Session.start(session_config)
            >>> session.security.basic_authentication.credentials
            {}
            >>> session.security.basic_authentication.credentials["elon"] = "X Æ A-12"
            >>> # The password can be changed:
            >>> session.security.basic_authentication.credentials["elon"] = "AE A-XII"
            >>> # But, for security reasons, it cannot be retrieved (accessing it will return a redacted string):
            >>> session.security.basic_authentication.credentials
            {'elon': '**REDACTED**'}
            >>> # Prevent user to authenticate through basic authentication:
            >>> del session.security.basic_authentication.credentials["elon"]
            >>> session.security.basic_authentication.credentials
            {}

            .. doctest::
                :hide:

                >>> del session
        """
        if self._credentials is None:
            raise RuntimeError("Credentials can only be managed on local sessions.")

        return self._credentials
