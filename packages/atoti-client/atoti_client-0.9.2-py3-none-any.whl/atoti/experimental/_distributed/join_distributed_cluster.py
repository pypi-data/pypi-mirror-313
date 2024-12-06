from __future__ import annotations

from ...cube import Cube
from .discovery_protocol import DiscoveryProtocol


def join_distributed_cluster(
    *,
    cube: Cube,
    distributed_session_url: str,
    distributed_cube_name: str,
    application_name: str | None = None,
    distributed_cube_port: int | None = None,
    data_cube_url: str | None = None,
    data_cube_port: int | None = None,
    discovery_protocol: DiscoveryProtocol | None = None,
) -> None:
    """Join the distributed cluster at the given address for the given distributed cube.

    Args:
        cube: The data cube joining the cluster.
        distributed_session_url: The URL of the distributed cluster.
        distributed_cube_name: The name of the query cube in the cluster.
        distributed_cube_port: The port of the query cube in the cluster.
        data_cube_url: The URL of the data cube joining the cluster.
        data_cube_port: The port of the data cube joining the cluster.
        discovery_protocol: The protocol used to discover the nodes of the cluster.
    """
    discovery_protocol_xml = (
        None if discovery_protocol is None else discovery_protocol._xml
    )
    cube._join_distributed_cluster(
        application_name=application_name or cube.name,
        query_cube_name=distributed_cube_name,
        query_cube_url=distributed_session_url,
        query_cube_port=distributed_cube_port,
        data_cube_url=data_cube_url,
        data_cube_port=data_cube_port,
        discovery_protocol_xml=discovery_protocol_xml,
    )
