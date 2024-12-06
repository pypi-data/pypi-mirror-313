from __future__ import annotations

from dataclasses import field
from typing import Literal, final

from pydantic.dataclasses import dataclass

from .._pydantic import PYDANTIC_CONFIG as _PYDANTIC_CONFIG
from .basic_authentication_config import BasicAuthenticationConfig
from .client_certificate_config import ClientCertificateConfig
from .https_config import HttpsConfig
from .jwt_config import JwtConfig
from .kerberos_config import KerberosConfig
from .ldap_config import LdapConfig
from .oidc_config import OidcConfig


@final
@dataclass(config=_PYDANTIC_CONFIG, frozen=True, kw_only=True)
class SecurityConfig:
    """The initial security config of the session.

    Note:
        This feature is not part of the community edition: it needs to be :doc:`unlocked </how_tos/unlock_all_features>`.

    Roles and restrictions can be configured with :attr:`atoti.Session.security`.
    """

    basic_authentication: BasicAuthenticationConfig = field(
        default_factory=BasicAuthenticationConfig,
    )
    """Always enabled even if :attr:`sso` is not ``None`` to facilitate the authentication of service/technical users."""

    client_certificate: ClientCertificateConfig | None = None

    https: HttpsConfig | None = None

    jwt: JwtConfig = field(default_factory=JwtConfig)

    same_site: Literal["lax", "none", "strict"] = "lax"
    """The value to use for the *SameSite* attribute of the HTTP cookie sent by the session.

    See https://web.dev/samesite-cookies-explained for more information.

    Note:
        ``"none"`` requires the session to be served over HTTPS.
    """

    sso: KerberosConfig | LdapConfig | OidcConfig | None = None
    """The config to delegate authentication to a Single Sign-On provider."""

    def __post_init__(self) -> None:
        if self.client_certificate and not self.https:
            raise ValueError(
                "Client certificate authentication requires HTTPS.",
            )
