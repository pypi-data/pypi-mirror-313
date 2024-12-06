from collections.abc import Collection
from typing import Literal

from ._server_versions import ServerVersions


def _get_supported_version_index(
    server_versions: ServerVersions,
    *,
    namespace: str,
    supported_versions: Collection[str],
) -> int:
    exposed_versions = tuple(
        version.id for version in server_versions.apis[namespace].versions
    )

    try:
        return next(
            index
            for index, version in enumerate(exposed_versions)
            if version in supported_versions
        )
    except StopIteration as error:
        raise RuntimeError(
            f"None of the available {namespace} versions {exposed_versions} match any of the supported ones {supported_versions}.",
        ) from error


_SUPPORTED_PIVOT_VERSIONS = ("9", "9zz1", "8", "8zz2", "8zz1", "7zz1", "6", "5", "4")
"""If a server exposes multiple pivot API versions, the first one in this collection will be used."""


def get_endpoint_path(
    *,
    attribute_name: Literal["restPath", "wsPath"] = "restPath",
    namespace: str,
    route: str,
    server_versions: ServerVersions,
) -> str:
    assert not route.startswith("/")
    assert (
        "?" not in route
    ), f"Expected the route to not contain a query string, but got `{route}`."

    version_index = (
        _get_supported_version_index(
            server_versions,
            namespace=namespace,
            supported_versions=_SUPPORTED_PIVOT_VERSIONS,
        )
        if namespace
        in {
            "activeviam/pivot",
            "pivot",  # Atoti Server < 6.0.0-M1.
        }
        else 0
    )

    version = server_versions.apis[namespace].versions[version_index]

    path: str | None

    match attribute_name:
        case "restPath":
            path = version.rest_path
        case "wsPath":
            path = version.ws_path

    if path is None:
        raise RuntimeError(f"Missing `{attribute_name}` for `{namespace}` namespace.")

    return f"{path.lstrip('/')}/{route}"
