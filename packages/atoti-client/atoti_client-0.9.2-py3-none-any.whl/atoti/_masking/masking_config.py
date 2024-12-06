from typing import Literal, final

from pydantic.dataclasses import dataclass

from .._constant import Constant
from .._identification import HierarchyIdentifier
from .._operation import Condition
from .._pydantic import PYDANTIC_CONFIG as _PYDANTIC_CONFIG


@final
@dataclass(config=_PYDANTIC_CONFIG, frozen=True, kw_only=True)
class MaskingConfig:
    only: (
        Condition[
            HierarchyIdentifier,
            Literal["eq", "isin"],
            Constant,
            Literal["and"] | None,
        ]
        | None
    ) = None
    exclude: (
        Condition[
            HierarchyIdentifier,
            Literal["eq", "isin"],
            Constant,
            Literal["and"] | None,
        ]
        | None
    ) = None
