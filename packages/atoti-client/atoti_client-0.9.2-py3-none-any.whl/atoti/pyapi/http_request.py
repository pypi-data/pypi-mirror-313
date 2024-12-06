from collections.abc import Mapping
from typing import final

from pydantic.dataclasses import dataclass

from .._pydantic import PYDANTIC_CONFIG as _PYDANTIC_CONFIG


@final
@dataclass(config=_PYDANTIC_CONFIG, frozen=True, kw_only=True)
class HttpRequest:
    """Info of an HTTP request."""

    url: str
    """URL on which the client request was made."""

    path_parameters: Mapping[str, str]
    """Mapping from the name of the path parameters to their value for this request."""

    body: object | None
    """Parsed JSON body of the request."""
