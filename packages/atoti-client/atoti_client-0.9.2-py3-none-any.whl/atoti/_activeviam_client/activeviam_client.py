from __future__ import annotations

import ssl
from collections.abc import Callable, Generator, Mapping
from contextlib import contextmanager
from mimetypes import types_map
from pathlib import Path
from typing import Annotated, Final, Literal, TypeVar, final

import httpx
from pydantic import BeforeValidator, ConfigDict, TypeAdapter
from pydantic.dataclasses import dataclass

from .._atoti_server_version import atoti_server_version
from .._collections import FrozenSequence
from .._pydantic import (
    PYDANTIC_CONFIG as __PYDANTIC_CONFIG,
    create_camel_case_alias_generator,
    get_type_adapter,
)
from ..authentication import Authenticate, ClientCertificate
from ._get_endpoint_path import get_endpoint_path
from ._get_server_versions import get_server_versions
from ._ping import ping
from ._server_versions import ServerVersions

_PYDANTIC_CONFIG: ConfigDict = {
    **__PYDANTIC_CONFIG,
    "alias_generator": create_camel_case_alias_generator(),
    "arbitrary_types_allowed": False,
    "extra": "ignore",
}


@final
@dataclass(config=_PYDANTIC_CONFIG, frozen=True, kw_only=True)
class _ErrorChainItem:
    message: str
    type: str


@final
@dataclass(config=_PYDANTIC_CONFIG, frozen=True, kw_only=True)
class _ConciseJsonResponseErrorBody:
    error: str
    path: str
    status: int


@final
@dataclass(config=_PYDANTIC_CONFIG, frozen=True, kw_only=True)
class _DetailedJsonResponseErrorBody:
    error_chain: FrozenSequence[_ErrorChainItem]
    stack_trace: str


_JsonResponseErrorBody = _ConciseJsonResponseErrorBody | _DetailedJsonResponseErrorBody


@final
class _JsonResponseError(httpx.HTTPStatusError):
    def __init__(
        self,
        body: _ConciseJsonResponseErrorBody | _DetailedJsonResponseErrorBody,
        /,
        *,
        request: httpx.Request,
        response: httpx.Response,
    ) -> None:
        message = (
            body.stack_trace
            if isinstance(body, _DetailedJsonResponseErrorBody)
            else body.error
        )
        super().__init__(message, request=request, response=response)


def _normalize_http_error_body(value: object, /) -> object:
    return (
        value.get("error")  # Atoti Server < 6.0.0-M1.
        if isinstance(value, dict) and value.get("status") == "error"
        else value
    )


def _enhance_json_response_raise_for_status(response: httpx.Response, /) -> None:
    if (
        response.is_success
        or response.headers.get("Content-Type") != types_map[".json"]
    ):
        return

    original_raise_for_status = response.raise_for_status

    def _enhanced_json_response_raise_for_status() -> httpx.Response:
        try:
            return original_raise_for_status()
        except httpx.HTTPStatusError as error:
            adapter: TypeAdapter[_JsonResponseErrorBody] = get_type_adapter(
                _ConciseJsonResponseErrorBody
                | Annotated[  # type: ignore[arg-type] # pyright: ignore[reportArgumentType]
                    _DetailedJsonResponseErrorBody,
                    # Remove when dropping support for Atoti Server < 6.0.0-M1.
                    BeforeValidator(_normalize_http_error_body),
                ],
            )
            body_json = response.read()
            body = adapter.validate_json(body_json)

            raise _JsonResponseError(
                body,
                request=error.request,
                response=error.response,
            ) from error

    response.raise_for_status = _enhanced_json_response_raise_for_status  # type: ignore[method-assign]


def _remove_cookies(request: httpx.Request, /) -> None:
    request.headers.pop("Cookie", None)


def _normalize_json_response_body(value: object, /) -> object:
    return (
        value.get("data")  # Atoti Server < 6.0.0-M1.
        if isinstance(value, dict) and value.get("status") == "success"
        else value
    )


_TypeT = TypeVar("_TypeT")


@final
class ActiveViamClient:
    """Client to communicate with ActiveViam servers such as Atoti Server or the Content Server."""

    @contextmanager
    @staticmethod
    def create(
        url: str,
        /,
        *,
        authentication: Authenticate | ClientCertificate | None = None,
        certificate_authority: Path | None = None,
        # Remove this parameter and always consider it `True` once distributed sessions can be pinged before the first query cube creation.
        ping: bool = True,
    ) -> Generator[ActiveViamClient, None, None]:
        authenticate: Authenticate | None = None

        auth: Callable[[httpx.Request], httpx.Request] | None = None
        verify: ssl.SSLContext | Literal[True] = True

        if certificate_authority is not None:
            verify = ssl.create_default_context(cafile=certificate_authority)

        match authentication:
            case None:
                ...
            case ClientCertificate():
                if not isinstance(verify, ssl.SSLContext):
                    verify = ssl.create_default_context()

                verify.load_cert_chain(
                    certfile=authentication.certificate,
                    keyfile=authentication.keyfile,
                    password=authentication.password,
                )

                def _authenticate(_: str, /) -> Mapping[str, str]:
                    raise RuntimeError(
                        "Cannot generate authentication headers from client certificate.",
                    )

                authenticate = _authenticate
            case _:

                def _auth(request: httpx.Request, /) -> httpx.Request:
                    headers = authentication(str(request.url))
                    request.headers.update(headers)
                    return request

                auth = _auth
                authenticate = authentication

        with httpx.Client(
            auth=auth,
            base_url=url,
            event_hooks={
                "request": [
                    # To make the client stateless.
                    # See https://github.com/encode/httpx/issues/2992.
                    _remove_cookies,
                ],
                "response": [
                    _enhance_json_response_raise_for_status,
                ],
            },
            verify=verify,
            timeout=None,
        ) as http_client:
            server_versions = get_server_versions(http_client=http_client)
            activeviam_client = ActiveViamClient(
                authenticate=authenticate,
                http_client=http_client,
                server_versions=server_versions,
            )
            if ping:
                # The `ping` endpoint is protected.
                # Calling it ensures that the client can authenticate against the server.
                activeviam_client.ping()
            yield activeviam_client

    # Remove when dropping support for Atoti Server < 6.0.0-M1.
    @staticmethod
    def get_json_response_body_type_adapter(
        body_type: type[_TypeT],
        /,
    ) -> TypeAdapter[_TypeT]:
        return get_type_adapter(
            Annotated[  # type: ignore[arg-type] # pyright: ignore[reportArgumentType]
                body_type,
                BeforeValidator(_normalize_json_response_body),
            ],
        )

    def __init__(
        self,
        *,
        authenticate: Authenticate | None,
        http_client: httpx.Client,
        server_versions: ServerVersions,
    ) -> None:
        self._authenticate: Final = authenticate
        self.http_client: Final = http_client
        self.server_versions: Final = server_versions

    @property
    def has_compatible_atoti_python_api_service(self) -> bool:
        return ("atoti" in self.server_versions.apis) and (
            self.server_versions.server_version == atoti_server_version()
        )

    @property
    def url(self) -> str:
        return str(self.http_client.base_url).rstrip("/")

    def generate_authentication_headers(self) -> Mapping[str, str]:
        return {} if self._authenticate is None else self._authenticate(self.url)

    def get_endpoint_path(
        self,
        *,
        attribute_name: Literal["restPath", "wsPath"] = "restPath",
        namespace: str,
        route: str,
    ) -> str:
        return get_endpoint_path(
            attribute_name=attribute_name,
            namespace=namespace,
            route=route,
            server_versions=self.server_versions,
        )

    def normalize_activeviam_namespace(self, namespace: str, /) -> str:
        return next(
            namespace
            for namespace in [
                f"activeviam/{namespace}",
                namespace,  # Atoti Server < 6.0.0-M1.
            ]
            if namespace in self.server_versions.apis
        )

    def ping(self) -> None:
        namespace = self.normalize_activeviam_namespace("pivot")
        path = self.get_endpoint_path(namespace=namespace, route="ping")
        ping(http_client=self.http_client, path=path)
