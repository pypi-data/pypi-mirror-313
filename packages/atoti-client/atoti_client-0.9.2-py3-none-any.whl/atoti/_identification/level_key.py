from typing import TypeAlias

from .dimension_name import DimensionName
from .hierarchy_name import HierarchyName
from .level_name import LevelName

LevelUnambiguousKey: TypeAlias = tuple[DimensionName, HierarchyName, LevelName]
LevelKey: TypeAlias = LevelName | tuple[HierarchyName, LevelName] | LevelUnambiguousKey
