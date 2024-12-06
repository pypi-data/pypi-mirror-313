from collections.abc import Set as AbstractSet
from typing import final

from pydantic.dataclasses import dataclass

from .._pydantic import PYDANTIC_CONFIG as _PYDANTIC_CONFIG


@final
@dataclass(config=_PYDANTIC_CONFIG, frozen=True, kw_only=True)
# Do not make this class public before solving these issues:
# - it should probably be renamed `ClusterConfig`.
# - `cube_port` makes no sense next to an attribute named `cube_url` as URLs must contain ports when they're not using the protocol's default one.
class DiscoveryConfig:
    allowed_application_names: AbstractSet[str]
    cube_name: str
    cube_url: str | None
    cube_port: int | None
    discovery_protocol_xml: str | None
