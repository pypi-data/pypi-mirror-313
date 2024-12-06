from pathlib import Path
from typing import final

from pydantic.dataclasses import dataclass

from .._pydantic import PYDANTIC_CONFIG as _PYDANTIC_CONFIG


@final
@dataclass(config=_PYDANTIC_CONFIG, frozen=True, kw_only=True)
class KerberosConfig:
    """The config to delegate authentication to `Kerberos <https://web.mit.edu/kerberos/>`__.

    The user's roles can be defined using :attr:`atoti.security.Security.kerberos` and :attr:`~atoti.security.Security.individual_roles`.

    Example:
        >>> from pathlib import Path
        >>> config = tt.KerberosConfig(
        ...     service_principal="HTTP/localhost",
        ...     keytab=Path("config") / "example.keytab",
        ...     krb5_config=Path("config") / "example.krb5",
        ... )
    """

    service_principal: str
    """The principal that the session will use."""

    keytab: Path | None = None
    """The path to the keytab file to use."""

    krb5_config: Path | None = None
    """The path to the Kerberos config file.

    Defaults to the OS-specific default location.
    """
