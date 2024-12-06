from typing import final

from pydantic.dataclasses import dataclass

from .._collections import FrozenSequence
from .._pydantic import PYDANTIC_CONFIG as _PYDANTIC_CONFIG


@final
@dataclass(config=_PYDANTIC_CONFIG, frozen=True, kw_only=True)
class User:
    """Info of a user calling a custom HTTP endpoint."""

    name: str
    """Name of the user calling the endpoint."""

    roles: FrozenSequence[str]
    """Roles of the user calling the endpoint."""
