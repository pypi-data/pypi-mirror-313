from __future__ import annotations

from collections.abc import Sequence

from .._identification import ColumnIdentifier, Identifiable, identify
from .._measure.consolidated_measure import ConsolidateMeasure
from .._measure_convertible import VariableMeasureConvertible
from .._measure_description import MeasureDescription, convert_to_measure_description
from ..hierarchy import Hierarchy


def consolidate(
    measure: VariableMeasureConvertible | str,
    /,
    *,
    hierarchy: Hierarchy,
    factors: Sequence[Identifiable[ColumnIdentifier]],
) -> MeasureDescription:
    columns = []
    for level_name in hierarchy:
        level = hierarchy[level_name]
        assert level._column_identifier
        columns.append(level._column_identifier)
    return ConsolidateMeasure(
        _underlying_measure=convert_to_measure_description(measure),
        _hierarchy=hierarchy._identifier,
        _level_columns=tuple(columns),
        _factors=tuple(identify(column) for column in factors),
    )
