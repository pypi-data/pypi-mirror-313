from __future__ import annotations

from collections.abc import Collection, Set as AbstractSet
from contextlib import AbstractContextManager, ExitStack
from pathlib import Path
from types import TracebackType
from typing import TYPE_CHECKING, Final, final

from typing_extensions import override

from ..._atoti_client import AtotiClient
from ..._java_api import JavaApi
from ..._started_session_resources import started_session_resources
from ...session_config.session_config import SessionConfig
from .discovery_protocol import DiscoveryProtocol

if TYPE_CHECKING:
    from _atoti_server import (  # pylint: disable=nested-import,undeclared-dependency
        ServerSubprocess,
    )


@final
class DistributedSession(AbstractContextManager["DistributedSession"]):
    """Do not make this class public before removing ``ActiveViamClient.create()``'s *ping* parameter."""

    @classmethod
    def start(
        cls,
        config: SessionConfig | None = None,
        /,
    ) -> DistributedSession:
        if config is None:
            config = SessionConfig()

        with ExitStack() as exit_stack:
            atoti_client, java_api, server_subprocess, _session_id = (
                exit_stack.enter_context(
                    started_session_resources(
                        address=None,
                        config=config,
                        enable_py4j_auth=True,
                        distributed=True,
                        py4j_server_port=None,
                        start_application=True,
                    ),
                )
            )
            assert server_subprocess is not None
            session = cls(
                atoti_client=atoti_client,
                java_api=java_api,
                server_subprocess=server_subprocess,
            )
            session._exit_stack.push(exit_stack.pop_all())
            return session

    def __init__(
        self,
        *,
        atoti_client: AtotiClient,
        java_api: JavaApi,
        server_subprocess: ServerSubprocess,
    ):
        self._atoti_client: Final = atoti_client
        self._exit_stack: Final = ExitStack()
        self._java_api: Final = java_api
        self._server_subprocess: Final = server_subprocess

    @override
    def __exit__(  # pylint: disable=too-many-positional-parameters
        self,
        exception_type: type[BaseException] | None,
        exception_value: BaseException | None,
        exception_traceback: TracebackType | None,
    ) -> None:
        self._exit_stack.__exit__(exception_type, exception_value, exception_traceback)

    def close(self) -> None:
        """Close this session and free all associated resources."""
        self.__exit__(None, None, None)

    def __del__(self) -> None:
        # Use private method to avoid sending a telemetry event that would raise `RuntimeError: cannot schedule new futures after shutdown` when calling `ThreadPoolExecutor.submit()`.
        self.__exit__(None, None, None)

    @property
    def logs_path(self) -> Path:
        return self._server_subprocess.logs_path

    @property
    def url(self) -> str:
        return self._atoti_client.activeviam_client.url

    def create_cube(
        self,
        name: str,
        *,
        allowed_application_names: AbstractSet[str],
        cube_url: str | None = None,
        cube_port: int | None = None,
        discovery_protocol: DiscoveryProtocol | None = None,
        distributing_levels: Collection[str] = (),
    ) -> None:
        """Create a distributed cube.

        Args:
            name: The name of the created cube.
            allowed_application_names: The names of the applications allowed to contribute to  this cube.
            cube_url: The URL of the cube.
            cube_port: The port of the cube.
            discovery_protocol: The protocol used to discover the nodes of the cluster.
            distributing_levels: The name of the levels partitioning the data within the cluster.
        """
        discovery_protocol_xml = (
            None if discovery_protocol is None else discovery_protocol._xml
        )
        self._java_api.create_distributed_cube(
            allowed_application_names=allowed_application_names,
            cube_name=name,
            cube_url=cube_url,
            cube_port=cube_port,
            discovery_protocol_xml=discovery_protocol_xml,
            distributing_levels=distributing_levels,
        )
        self._java_api.java_api.refresh()
