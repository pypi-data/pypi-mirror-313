from __future__ import annotations

from typing import Literal

from ._constant import Constant
from ._identification import HierarchyIdentifier, LevelIdentifier
from ._operation import Condition, ConditionComparisonOperatorBound

QueryFilter = Condition[
    HierarchyIdentifier | LevelIdentifier,
    ConditionComparisonOperatorBound,
    Constant,
    Literal["and"] | None,
]
