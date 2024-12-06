from __future__ import annotations

from collections.abc import Mapping, Set as AbstractSet
from typing import Final, final

from typing_extensions import override

from ._collections import DelegatingMutableMapping
from ._java_api import JavaApi
from .security._authentication_type import AuthenticationType

_BASIC_AUTHENTICATION_TYPE: AuthenticationType = "BASIC"
_REDACTED_PASSWORD = "**REDACTED**"  # noqa: S105


@final
class BasicCredentials(DelegatingMutableMapping[str, str]):
    def __init__(self, *, java_api: JavaApi) -> None:
        self._java_api: Final = java_api

    @override
    def _get_delegate(self, *, key: str | None) -> Mapping[str, str]:
        return {
            username: _REDACTED_PASSWORD
            for username in self._java_api._enterprise_api().getUsers(
                _BASIC_AUTHENTICATION_TYPE,
            )
            if key is None or username == key
        }

    @override
    def _update_delegate(self, other: Mapping[str, str], /) -> None:
        usernames = set(self)

        for username, password in other.items():
            if username in usernames:
                self._java_api._enterprise_api().updateUserPassword(
                    username,
                    password,
                    _BASIC_AUTHENTICATION_TYPE,
                )
            else:
                self._java_api._enterprise_api().createUser(
                    username,
                    password,
                    _BASIC_AUTHENTICATION_TYPE,
                )

    @override
    def _delete_delegate_keys(self, keys: AbstractSet[str], /) -> None:
        for username in keys:
            self._java_api._enterprise_api().deleteUser(
                username,
                _BASIC_AUTHENTICATION_TYPE,
            )
