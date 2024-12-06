from .._activeviam_client import ActiveViamClient
from .._cube_discovery import CubeDiscovery


def get_cube_discovery(
    *,
    activeviam_client: ActiveViamClient,
    pivot_namespace: str,
) -> CubeDiscovery:
    path = activeviam_client.get_endpoint_path(
        namespace=pivot_namespace,
        route="cube/discovery",
    )
    response = activeviam_client.http_client.get(path).raise_for_status()
    body = response.content
    return activeviam_client.get_json_response_body_type_adapter(
        CubeDiscovery,
    ).validate_json(body)
