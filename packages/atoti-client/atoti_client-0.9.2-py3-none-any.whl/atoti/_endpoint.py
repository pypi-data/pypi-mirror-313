from __future__ import annotations

import json
from collections.abc import Callable, Collection
from typing import TYPE_CHECKING, Any, Final, final

from py4j.java_collections import JavaMap

from ._py4j_utils import to_python_dict
from .pyapi.http_request import HttpRequest
from .pyapi.user import User

if TYPE_CHECKING:
    from .session import Session  # pylint: disable=nested-import

    CallbackEndpoint = Callable[[HttpRequest, User, Session], Any]


@final
class EndpointHandler:
    def __init__(self, callback: CallbackEndpoint, /, *, session: Session) -> None:
        self._callback: Final = callback
        self._session: Final = session

    def handleRequest(  # noqa: N802, pylint: disable=too-many-positional-parameters
        self,
        url: str,
        username: str,
        roles: str,
        path_parameter_values: JavaMap,
        body: str | None = None,
    ) -> str:
        path_parameters = {
            str(key): str(value)
            for key, value in to_python_dict(path_parameter_values).items()
        }
        parsed_body = None if body is None else json.loads(body)
        request = HttpRequest(
            url=url,
            path_parameters=path_parameters,
            body=parsed_body,
        )
        user = User(name=username, roles=roles[1 : len(roles) - 1].split(", "))

        response_body = self._callback(
            request,
            user,
            self._session,
        )

        return json.dumps(response_body)

    def toString(self) -> str:  # noqa: N802
        return "Python.EndpointHandler"

    @final
    class Java:
        """Code needed for Py4J callbacks."""

        implements: Collection[str] = ["io.atoti.runtime.api.pyapi.EndpointHandler"]
