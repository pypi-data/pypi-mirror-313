from dataclasses import KW_ONLY
from typing import final

from pydantic.dataclasses import dataclass
from typing_extensions import override

from ._identifier_pydantic_config import IDENTIFIER_PYDANTIC_CONFIG
from .identifier import Identifier
from .measure_name import MeasureName


@final
@dataclass(config=IDENTIFIER_PYDANTIC_CONFIG, frozen=True)
class MeasureIdentifier(Identifier):
    measure_name: MeasureName
    _: KW_ONLY

    @override
    def __repr__(self) -> str:
        return f"""m["{self.measure_name}"]"""
