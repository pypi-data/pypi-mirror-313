from dataclasses import dataclass
from typing import final

from typing_extensions import override

from .._identification import LevelIdentifier, MeasureIdentifier
from .._java_api import JavaApi
from .._measure_description import MeasureDescription
from .utils import get_measure_name


@final
@dataclass(eq=False, frozen=True, kw_only=True)
class DateShift(MeasureDescription):
    """Shift the value."""

    _underlying_measure: MeasureDescription
    _level_identifier: LevelIdentifier
    _shift: str
    _method: str

    @override
    def _do_distil(
        self,
        identifier: MeasureIdentifier | None = None,
        /,
        *,
        java_api: JavaApi,
        cube_name: str,
    ) -> MeasureIdentifier:
        underlying_name = get_measure_name(
            java_api=java_api,
            measure=self._underlying_measure,
            cube_name=cube_name,
        )
        return java_api.create_measure(
            identifier,
            "DATE_SHIFT",
            underlying_name,
            self._level_identifier._java_description,
            self._shift,
            self._method,
            cube_name=cube_name,
        )
