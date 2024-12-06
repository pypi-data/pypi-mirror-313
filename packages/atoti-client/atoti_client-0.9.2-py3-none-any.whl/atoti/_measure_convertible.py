from __future__ import annotations

from typing_extensions import TypeIs

from ._constant import Constant, ConstantValue
from ._identification import (
    HasIdentifier,
    HierarchyIdentifier,
    LevelIdentifier,
    MeasureIdentifier,
)
from ._operation import (
    Condition,
    ConditionBound,
    ConditionCombinationOperatorBound,
    ConditionComparisonOperatorBound,
    Operation,
    OperationBound,
)

MeasureConvertibleIdentifier = HierarchyIdentifier | LevelIdentifier | MeasureIdentifier

MeasureOperation = Operation[MeasureConvertibleIdentifier]

MeasureCondition = Condition[
    HierarchyIdentifier | MeasureConvertibleIdentifier | MeasureOperation,
    ConditionComparisonOperatorBound,
    Constant | MeasureConvertibleIdentifier | MeasureOperation | None,
    ConditionCombinationOperatorBound,
]

VariableMeasureOperand = (
    MeasureCondition | MeasureOperation | MeasureConvertibleIdentifier
)
MeasureOperand = Constant | VariableMeasureOperand

VariableMeasureConvertible = (
    HasIdentifier[MeasureConvertibleIdentifier] | MeasureCondition | MeasureOperation
)
MeasureConvertible = ConstantValue | VariableMeasureConvertible


def _is_measure_base_operation(value: ConditionBound | OperationBound, /) -> bool:
    # It is not a measure `BaseOperation` if there are some unexpected identifier types.
    return not (
        value._identifier_types
        - {HierarchyIdentifier, LevelIdentifier, MeasureIdentifier}
    )


def is_measure_condition(value: object, /) -> TypeIs[MeasureCondition]:
    return isinstance(value, Condition) and _is_measure_base_operation(value)


def is_measure_operation(value: object, /) -> TypeIs[MeasureOperation]:
    return isinstance(value, Operation) and _is_measure_base_operation(value)


def is_measure_condition_or_operation(
    value: object,
    /,
) -> TypeIs[MeasureCondition | MeasureOperation]:
    return (
        is_measure_condition(value)
        if isinstance(value, Condition)
        else is_measure_operation(value)
    )


def is_variable_measure_convertible(
    value: object,
    /,
) -> TypeIs[VariableMeasureConvertible]:
    return (
        isinstance(
            value._identifier,
            HierarchyIdentifier | LevelIdentifier | MeasureIdentifier,
        )
        if isinstance(value, HasIdentifier)
        else is_measure_condition_or_operation(value)
    )
