from __future__ import annotations

from typing import Literal

from ._constant import Constant
from ._identification import LevelIdentifier
from ._operation import Condition

GaqFilter = Condition[
    LevelIdentifier,
    Literal["eq", "isin", "ne"],
    Constant,
    Literal["and"] | None,
]
