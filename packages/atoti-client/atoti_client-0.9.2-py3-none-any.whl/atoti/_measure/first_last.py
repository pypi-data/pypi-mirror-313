from dataclasses import dataclass
from typing import Literal, final

from typing_extensions import override

from .._identification import LevelIdentifier, MeasureIdentifier
from .._java_api import JavaApi
from .._measure_description import MeasureDescription
from .utils import get_measure_name


@final
@dataclass(eq=False, frozen=True, kw_only=True)
class FirstLast(MeasureDescription):
    """Shift the value."""

    _underlying_measure: MeasureDescription
    _level_identifier: LevelIdentifier
    _mode: Literal["FIRST", "LAST"]
    _partitioning: LevelIdentifier | None

    @override
    def _do_distil(
        self,
        identifier: MeasureIdentifier | None = None,
        /,
        *,
        cube_name: str,
        java_api: JavaApi,
    ) -> MeasureIdentifier:
        underlying_name = get_measure_name(
            java_api=java_api,
            measure=self._underlying_measure,
            cube_name=cube_name,
        )
        return java_api.create_measure(
            identifier,
            "FIRST_LAST",
            underlying_name,
            self._level_identifier._java_description,
            self._mode,
            self._partitioning._java_description
            if self._partitioning is not None
            else None,
            cube_name=cube_name,
        )
