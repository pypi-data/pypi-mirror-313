from __future__ import annotations

from dataclasses import KW_ONLY, dataclass
from typing import final

from typing_extensions import override

from .._identification import MeasureIdentifier
from .._java_api import JavaApi
from .._measure_description import MeasureDescription
from .utils import convert_measure_args


@final
@dataclass(eq=False, frozen=True)
class BooleanMeasure(MeasureDescription):
    """Boolean operation between measures."""

    _operator: str
    _operands: tuple[MeasureDescription, ...]
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
        return java_api.create_measure(
            identifier,
            "BOOLEAN",
            self._operator,
            convert_measure_args(
                java_api=java_api,
                cube_name=cube_name,
                args=self._operands,
            ),
            cube_name=cube_name,
        )
