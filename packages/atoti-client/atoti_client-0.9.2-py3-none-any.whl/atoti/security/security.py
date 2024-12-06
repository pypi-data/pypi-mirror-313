from __future__ import annotations

from collections.abc import MutableMapping
from typing import Final, final

from typing_extensions import deprecated

from .._activeviam_client import ActiveViamClient
from .._content_client import ContentClient
from .._deprecated_warning_category import (
    DEPRECATED_WARNING_CATEGORY as _DEPRECATED_WARNING_CATEGORY,
)
from ._restriction import Restriction
from ._restrictions import Restrictions
from ._service import Service
from .basic_authentication_security import BasicAuthenticationSecurity
from .default_roles import DefaultRoles
from .individual_roles import IndividualRoles
from .kerberos_security import KerberosSecurity
from .ldap_security import LdapSecurity
from .oidc_security import OidcSecurity
from .role_mapping import RoleMapping


@final
class Security:
    """Manage the parts of the security config that can be changed without restarting the :class:`~atoti.Session`.

    The roles and restrictions are stored in the :attr:`~atoti.SessionConfig.user_content_storage`.
    Multiple sessions configured with the same user content storage will thus share their roles and restrictions.

    Note:
        Users without the :guilabel:`ROLE_USER` will not be able to access the application.
    """

    def __init__(
        self,
        *,
        activeviam_client: ActiveViamClient,
        basic_credentials: MutableMapping[str, str] | None = None,
    ):
        if not activeviam_client.has_compatible_atoti_python_api_service:
            # Sessions started with the Java API ignore the restrictions and roles stored by Atoti Python API in the user content storage.
            # Managing security on such sessions is forbidden to avoid users being confused with their changes having no impact.
            raise RuntimeError(
                "Cannot manage security on a session that was not created with Atoti Python API.",
            )

        self._basic_credentials: Final = basic_credentials
        self._service: Final = Service(
            content_client=ContentClient(activeviam_client=activeviam_client),
        )

    @property
    def restrictions(self) -> MutableMapping[str, Restriction]:
        """Mapping from role name to corresponding restriction.

        Restrictions limit the data accessible to users based on their roles.
        Restrictions apply on table columns and are inherited by all hierarchies based on these columns.

        * Restrictions on different columns/hierarchies are intersected.
        * Restrictions on the same column/hierarchy are unioned.

        See the example below for an illustration.

        Note:
            :guilabel:`ROLE_USER` and :guilabel:`ROLE_ADMIN` are reserved roles for which restrictions cannot be declared.

            :guilabel:`ROLE_ADMIN` always grants full access to the application (read, write, delete, etc.).

        Example:
            >>> session_config = tt.SessionConfig(security=tt.SecurityConfig())
            >>> session = tt.Session.start(session_config)
            >>> df = pd.DataFrame(
            ...     [
            ...         ("Asia", "Korea", "KRW"),
            ...         ("Asia", "Japan", "JPY"),
            ...         ("Europe", "France", "EUR"),
            ...         ("Europe", "Germany", "EUR"),
            ...         ("Europe", "Norway", "NOK"),
            ...         ("Europe", "Sweden", "SEK"),
            ...     ],
            ...     columns=["Continent", "Country", "Currency"],
            ... )
            >>> table = session.read_pandas(
            ...     df,
            ...     keys={"Continent", "Country", "Currency"},
            ...     table_name="Restrictions example",
            ... )
            >>> cube = session.create_cube(table)
            >>> h, l, m = cube.hierarchies, cube.levels, cube.measures
            >>> cube.hierarchies["Geography"] = [
            ...     table["Continent"],
            ...     table["Country"],
            ... ]
            >>> for level_name in cube.hierarchies["Geography"]:
            ...     del cube.hierarchies[level_name]
            >>> username, password = "john", "abcdef123456"
            >>> session.security.basic_authentication.credentials[username] = password

            The user initially has no individual roles:

            >>> username in session.security.individual_roles
            False

            Adding :guilabel:`ROLE_USER` grants access to the application:

            >>> session.security.individual_roles[username] = {"ROLE_USER"}
            >>> connected_session = tt.Session.connect(
            ...     session.url,
            ...     authentication=tt.BasicAuthentication(username, password),
            ... )
            >>> cube = connected_session.cubes[cube.name]
            >>> h, l, m = cube.hierarchies, cube.levels, cube.measures

            :guilabel:`ROLE_USER` has no restrictions so all the countries and currencies are accessible:

            >>> cube.query(m["contributors.COUNT"], levels=[l["Country"], l["Currency"]])
                                       contributors.COUNT
            Continent Country Currency
            Asia      Japan   JPY                       1
                      Korea   KRW                       1
            Europe    France  EUR                       1
                      Germany EUR                       1
                      Norway  NOK                       1
                      Sweden  SEK                       1

            Assigning a role to the user to limit access to :guilabel:`France` only:

            >>> session.security.restrictions["ROLE_FRANCE"] = table["Country"] == "France"
            >>> session.security.individual_roles[username] |= {"ROLE_FRANCE"}
            >>> cube.query(m["contributors.COUNT"], levels=[l["Country"]])
                              contributors.COUNT
            Continent Country
            Europe    France                   1

            In the code block below, :guilabel:`ROLE_FRANCE` and :guilabel:`ROLE_GERMANY` individually limit access to, respectively, :guilabel:`France` only and :guilabel:`Germany` only.
            However, when a user has both, the union of the sets are accessible.

            >>> session.security.restrictions["ROLE_GERMANY"] = (
            ...     table["Country"] == "Germany"
            ... )
            >>> session.security.individual_roles[username] |= {"ROLE_GERMANY"}
            >>> cube.query(m["contributors.COUNT"], levels=[l["Country"]])
                              contributors.COUNT
            Continent Country
            Europe    France                   1
                      Germany                  1

            Restrictions can include multiple elements:

            >>> session.security.restrictions["ROLE_NORDIC"] = table["Country"].isin(
            ...     "Norway", "Sweden"
            ... )
            >>> session.security.individual_roles[username] |= {"ROLE_NORDIC"}
            >>> cube.query(m["contributors.COUNT"], levels=[l["Country"]])
                              contributors.COUNT
            Continent Country
            Europe    France                   1
                      Germany                  1
                      Norway                   1
                      Sweden                   1

            Since :guilabel:`Country` and :guilabel:`Continent` are part of the same :guilabel:`Geography` hierarchy, restrictions on these two levels are unioned:

            >>> session.security.restrictions["ROLE_ASIA"] = table["Continent"] == "Asia"
            >>> session.security.individual_roles[username] |= {"ROLE_ASIA"}
            >>> cube.query(m["contributors.COUNT"], levels=[l["Country"]])
                              contributors.COUNT
            Continent Country
            Asia      Japan                    1
                      Korea                    1
            Europe    France                   1
                      Germany                  1
                      Norway                   1
                      Sweden                   1

            :guilabel:`Currency` is part of a different hierarchy so restrictions on it are intersected with the ones from :guilabel:`Geography`:

            >>> session.security.restrictions["ROLE_EUR"] = table["Currency"] == "EUR"
            >>> session.security.individual_roles[username] |= {"ROLE_EUR"}
            >>> cube.query(m["contributors.COUNT"], levels=[l["Country"], l["Currency"]])
                                       contributors.COUNT
            Continent Country Currency
            Europe    France  EUR                       1
                      Germany EUR                       1

            Removing the :guilabel:`ROLE_FRANCE` and :guilabel:`ROLE_GERMANY` roles leaves no remaining accessible countries:

            >>> session.security.individual_roles[username] -= {
            ...     "ROLE_FRANCE",
            ...     "ROLE_GERMANY",
            ... }
            >>> cube.query(m["contributors.COUNT"], levels=[l["Country"]])
            Empty DataFrame
            Columns: [contributors.COUNT]
            Index: []

            .. doctest::
                :hide:

                >>> del session

        """
        return Restrictions(service=self._service)

    @property
    def individual_roles(self) -> IndividualRoles:
        return IndividualRoles(service=self._service)

    @property
    @deprecated(
        "`security.basic` is deprecated, use `security.basic_authentication` instead.",
        category=_DEPRECATED_WARNING_CATEGORY,
    )
    def basic(self) -> BasicAuthenticationSecurity:
        """The basic authentication security.

        :meta private:
        """
        return self.basic_authentication

    @property
    def basic_authentication(self) -> BasicAuthenticationSecurity:
        return BasicAuthenticationSecurity(
            credentials=self._basic_credentials,
            service=self._service,
        )

    @property
    def kerberos(self) -> KerberosSecurity:
        return KerberosSecurity(
            default_roles=DefaultRoles(
                authentication_type="KERBEROS",
                service=self._service,
            ),
            service=self._service,
        )

    @property
    def ldap(self) -> LdapSecurity:
        return LdapSecurity(
            default_roles=DefaultRoles(
                authentication_type="LDAP",
                service=self._service,
            ),
            role_mapping=RoleMapping(
                authentication_type="LDAP",
                service=self._service,
            ),
            service=self._service,
        )

    @property
    def oidc(self) -> OidcSecurity:
        return OidcSecurity(
            default_roles=DefaultRoles(
                authentication_type="OIDC",
                service=self._service,
            ),
            role_mapping=RoleMapping(
                authentication_type="OIDC",
                service=self._service,
            ),
            service=self._service,
        )

    def _clear(self) -> None:
        if self._basic_credentials is not None:
            self._basic_credentials.clear()

        self._service.clear()
