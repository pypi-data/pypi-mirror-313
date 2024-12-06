from __future__ import annotations

from typing import Literal

from .._constant import Constant
from .._identification import ColumnIdentifier
from .._operation import Condition

Restriction = Condition[
    ColumnIdentifier,
    Literal["eq", "isin"],
    Constant,
    Literal["and"] | None,
]
