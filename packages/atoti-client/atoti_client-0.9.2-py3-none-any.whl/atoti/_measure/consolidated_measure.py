from dataclasses import dataclass
from typing import final

from typing_extensions import override

from .._identification import (
    ColumnIdentifier,
    HierarchyIdentifier,
    MeasureIdentifier,
)
from .._java_api import JavaApi
from .._measure.utils import get_measure_name
from .._measure_description import MeasureDescription
from .._py4j_utils import to_java_list


@final
@dataclass(eq=False, frozen=True, kw_only=True)
class ConsolidateMeasure(MeasureDescription):
    _underlying_measure: MeasureDescription | str
    _hierarchy: HierarchyIdentifier
    _level_columns: tuple[ColumnIdentifier, ...]
    _factors: tuple[ColumnIdentifier, ...]

    @override
    def _do_distil(
        self,
        identifier: MeasureIdentifier | None = None,
        /,
        *,
        java_api: JavaApi,
        cube_name: str,
    ) -> MeasureIdentifier:
        underlying_name = (
            self._underlying_measure
            if isinstance(self._underlying_measure, str)
            else get_measure_name(
                java_api=java_api,
                measure=self._underlying_measure,
                cube_name=cube_name,
            )
        )

        return java_api.create_measure(
            identifier,
            "ALTERNATE_HIERARCHY_MEASURE",
            underlying_name,
            self._hierarchy._java_description,
            self._factors[0].table_identifier.table_name,
            to_java_list(
                [column.column_name for column in self._level_columns],
                gateway=java_api.gateway,
            ),
            to_java_list(
                [column.column_name for column in self._factors],
                gateway=java_api.gateway,
            ),
            cube_name=cube_name,
        )
