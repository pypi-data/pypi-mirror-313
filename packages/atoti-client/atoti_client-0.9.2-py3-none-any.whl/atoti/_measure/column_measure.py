from dataclasses import dataclass
from typing import final

from typing_extensions import override

from .._identification import ColumnIdentifier, MeasureIdentifier
from .._java_api import JavaApi
from .._measure_description import MeasureDescription


@final
@dataclass(eq=False, frozen=True, kw_only=True)
class ColumnMeasure(MeasureDescription):
    """Measure based on the column of a table."""

    _column_identifier: ColumnIdentifier
    _plugin_key: str

    @override
    def _do_distil(
        self,
        identifier: MeasureIdentifier | None = None,
        /,
        *,
        cube_name: str,
        java_api: JavaApi,
    ) -> MeasureIdentifier:
        return java_api.aggregated_measure(
            identifier,
            self._plugin_key,
            column_identifier=self._column_identifier,
            cube_name=cube_name,
        )
