from __future__ import annotations

from collections.abc import Mapping, Sequence, Set as AbstractSet
from typing import Any, overload

from .._constant import ConstantValue
from .._identification import ColumnIdentifier, Identifiable, identify
from .._measure.copy_measure import CopyMeasure, FullCopyMeasure
from .._measure_convertible import VariableMeasureConvertible
from .._measure_description import MeasureDescription, convert_to_measure_description
from ..hierarchy import Hierarchy


@overload
def copy(
    measure: VariableMeasureConvertible | str,
    /,
    *,
    source: Mapping[Hierarchy, list[Any]],
    target: Mapping[Hierarchy, list[list[Any]]],
) -> MeasureDescription: ...


@overload
def copy(
    measure: VariableMeasureConvertible,
    /,
    *,
    hierarchy: Hierarchy,
    member_paths: Mapping[
        tuple[ConstantValue, ...],
        AbstractSet[tuple[ConstantValue, ...]],
    ],
    consolidation_factors: Sequence[Identifiable[ColumnIdentifier]] = (),
) -> MeasureDescription: ...


def copy(
    measure: VariableMeasureConvertible | str,
    /,
    *,
    hierarchy: Hierarchy | None = None,
    member_paths: Mapping[
        tuple[ConstantValue, ...],
        AbstractSet[tuple[ConstantValue, ...]],
    ]
    | None = None,
    consolidation_factors: Sequence[Identifiable[ColumnIdentifier]] = (),
    source: Mapping[Hierarchy, list[Any]] | None = None,
    target: Mapping[Hierarchy, list[list[Any]]] | None = None,
) -> MeasureDescription:
    if hierarchy is not None or member_paths is not None or consolidation_factors:
        assert hierarchy is not None
        assert member_paths is not None
        columns = []
        for level_name in hierarchy:
            level = hierarchy[level_name]
            assert level._column_identifier
            columns.append(level._column_identifier)

        return FullCopyMeasure(
            _underlying_measure=convert_to_measure_description(measure),
            _hierarchy=hierarchy._identifier,
            _hierarchy_columns=tuple(columns),
            _member_paths=member_paths,
            _consolidation_factors=tuple(
                identify(column) for column in consolidation_factors
            ),
        )

    assert source is not None
    assert target is not None

    return CopyMeasure(
        _underlying_measure=measure
        if isinstance(measure, str)
        else convert_to_measure_description(measure),
        _source={
            hierarchy._identifier: location for hierarchy, location in source.items()
        },
        _target={
            hierarchy._identifier: location for hierarchy, location in target.items()
        },
    )
