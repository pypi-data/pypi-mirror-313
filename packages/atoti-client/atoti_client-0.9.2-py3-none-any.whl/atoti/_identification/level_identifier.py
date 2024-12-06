from dataclasses import KW_ONLY
from typing import final

from pydantic.dataclasses import dataclass
from typing_extensions import Self, override

from ._identifier_pydantic_config import IDENTIFIER_PYDANTIC_CONFIG
from .dimension_name import DimensionName
from .hierarchy_identifier import HierarchyIdentifier
from .hierarchy_name import HierarchyName
from .identifier import Identifier
from .level_name import LevelName


@final
@dataclass(config=IDENTIFIER_PYDANTIC_CONFIG, frozen=True)
class LevelIdentifier(Identifier):
    hierarchy_identifier: HierarchyIdentifier
    level_name: LevelName
    _: KW_ONLY

    @classmethod
    def _parse_java_description(cls, java_description: str, /) -> Self:
        level_name, hierarchy_name, dimension_name = java_description.split("@")
        return cls(HierarchyIdentifier(dimension_name, hierarchy_name), level_name)

    @property
    def _java_description(self) -> str:
        return "@".join(reversed(self.key))

    @property
    def key(self) -> tuple[DimensionName, HierarchyName, LevelName]:
        return *self.hierarchy_identifier.key, self.level_name

    @override
    def __repr__(self) -> str:
        return f"l[{self.key}]"
