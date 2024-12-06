from __future__ import annotations

from dataclasses import KW_ONLY, dataclass
from typing import final

from typing_extensions import override

from .._identification import MeasureIdentifier
from .._java_api import JavaApi
from .._measure_description import MeasureDescription


@final
@dataclass(eq=False, frozen=True)
class PublishedMeasure(MeasureDescription):
    _name: str
    _: KW_ONLY

    @override
    def _do_distil(
        self,
        identifier: MeasureIdentifier | None = None,
        /,
        *,
        cube_name: str,
        java_api: JavaApi,
    ) -> MeasureIdentifier:
        raise RuntimeError("Cannot create a measure that already exists in the cube.")
