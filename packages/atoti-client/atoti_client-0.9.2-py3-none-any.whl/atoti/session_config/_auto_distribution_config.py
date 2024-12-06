from typing import final

from pydantic.dataclasses import dataclass

from .._collections import FrozenSequence
from .._pydantic import PYDANTIC_CONFIG as _PYDANTIC_CONFIG
from ._discovery_config import DiscoveryConfig


@final
@dataclass(config=_PYDANTIC_CONFIG, frozen=True, kw_only=True)
class AutoDistributionConfig:
    """The config to automatically join a distributed cluster.

    Note:
        This feature is not part of the community edition: it needs to be :doc:`unlocked </how_tos/unlock_all_features>`.
    """

    data_cube_url: str
    clusters: FrozenSequence[DiscoveryConfig]
