from __future__ import annotations

import math
from abc import abstractmethod
from collections.abc import Sequence
from dataclasses import dataclass
from typing import cast, final

from typing_extensions import override

from ._constant import Constant
from ._identification import (
    HasIdentifier,
    HierarchyIdentifier,
    Identifier,
    LevelIdentifier,
    MeasureIdentifier,
)
from ._java_api import JavaApi
from ._measure_convertible import MeasureConvertible, MeasureOperand
from ._operation import (
    ArithmeticOperation,
    CombinedCondition,
    ComparisonCondition,
    Condition,
    HierarchyIsinCondition,
    IndexingOperation,
    IsinCondition,
    Operation,
)


@dataclass(eq=False, frozen=True, kw_only=True)
class MeasureDescription(Operation[MeasureIdentifier]):
    """The description of a :class:`~atoti.Measure` that has not been added to the cube yet."""

    @final
    def _distil(
        self,
        identifier: MeasureIdentifier | None = None,
        /,
        *,
        java_api: JavaApi,
        cube_name: str,
    ) -> MeasureIdentifier:
        """Return the identifier of the measure, creating it in the cube if it does not exist yet."""
        name: str | None = self.__dict__.get("_name")
        if not name:
            name = self._do_distil(
                identifier,
                java_api=java_api,
                cube_name=cube_name,
            ).measure_name
            self.__dict__["_name"] = name
        elif identifier:
            # This measure has already been distilled, this is a copy with a different name.
            java_api.copy_measure(
                MeasureIdentifier(name),
                identifier,
                cube_name=cube_name,
            )
        assert isinstance(name, str)
        return MeasureIdentifier(name)

    @abstractmethod
    def _do_distil(
        self,
        identifier: MeasureIdentifier | None = None,
        /,
        *,
        java_api: JavaApi,
        cube_name: str,
    ) -> MeasureIdentifier:
        """Create the measure in the cube and return its identifier."""

    @property
    @override
    def _identifier_types(self) -> frozenset[type[Identifier]]:
        return frozenset([MeasureIdentifier])


def convert_operand_to_measure_description(
    value: MeasureOperand | None,
    /,
) -> MeasureDescription:
    # pylint: disable=nested-import
    from ._measure.hierarchy_measure import HierarchyMeasure
    from ._measure.level_measure import LevelMeasure
    from ._measure.published_measure import PublishedMeasure

    # pylint: enable=nested-import

    if value is None:
        raise TypeError(
            f"Cannot convert `{value}` operand to `{MeasureDescription.__name__}`.",
        )

    if isinstance(value, HierarchyIdentifier):
        return HierarchyMeasure(value)

    if isinstance(value, LevelIdentifier):
        return LevelMeasure(value)

    if isinstance(value, MeasureIdentifier):
        return PublishedMeasure(value.measure_name)

    return convert_to_measure_description(
        value.value if isinstance(value, Constant) else cast(MeasureConvertible, value),
    )


def convert_to_measure_description(  # noqa: C901, PLR0911, PLR0912
    value: MeasureConvertible,
    /,
) -> MeasureDescription:
    # pylint: disable=nested-import
    from ._measure.boolean_measure import BooleanMeasure
    from ._measure.calculated_measure import CalculatedMeasure, Operator
    from ._measure.constant_measure import ConstantMeasure
    from ._measure.hierarchy_measure import HierarchyMeasure
    from ._measure.level_measure import LevelMeasure
    from ._measure.published_measure import PublishedMeasure

    # pylint: enable=nested-import

    if isinstance(value, MeasureDescription):
        return value

    if isinstance(value, Condition):
        if isinstance(value, CombinedCondition):
            return BooleanMeasure(
                value.boolean_operator,
                tuple(
                    convert_to_measure_description(operand)
                    for operand in value.sub_conditions
                ),
            )

        if isinstance(value, ComparisonCondition):
            assert not isinstance(
                value.subject,
                HierarchyIdentifier,
            ), f"Instances of `{HierarchyIsinCondition.__name__}` should have been converted to combined `{ComparisonCondition.__name__}`s."

            subject = convert_operand_to_measure_description(value.subject)
            if value.target is None:
                return BooleanMeasure(
                    "isNull" if value.operator == "eq" else "notNull",
                    (subject,),
                )
            return BooleanMeasure(
                value.operator,
                (
                    subject,
                    convert_operand_to_measure_description(value.target),
                ),
            )

        if isinstance(value, HierarchyIsinCondition | IsinCondition):
            return convert_to_measure_description(value.combined_comparison_condition)

        raise TypeError(f"Unexpected condition type: `{type(value)}`.")

    if isinstance(value, HasIdentifier):
        identifier = value._identifier

        if isinstance(identifier, LevelIdentifier):
            return LevelMeasure(identifier)

        if isinstance(identifier, HierarchyIdentifier):
            return HierarchyMeasure(identifier)

        assert isinstance(identifier, MeasureIdentifier)
        return PublishedMeasure(identifier.measure_name)

    if isinstance(value, Operation):
        if isinstance(value, ArithmeticOperation):
            return CalculatedMeasure(
                Operator(
                    value.operator,
                    [
                        convert_operand_to_measure_description(operand)
                        for operand in value.operands
                    ],
                ),
            )

        if isinstance(value, IndexingOperation):
            if isinstance(value.index, slice):
                if value.index.step:
                    raise ValueError(
                        "Cannot index an array measure using a slice with a step.",
                    )
                start = value.index.start if value.index.start is not None else 0
                stop = value.index.stop if value.index.stop is not None else math.inf
                return CalculatedMeasure(
                    Operator(
                        "vector_sub",
                        [
                            convert_operand_to_measure_description(value.operand),
                            convert_to_measure_description(start),
                            convert_to_measure_description(stop),
                        ],
                    ),
                )

            return CalculatedMeasure(
                Operator(
                    "vector_element",
                    [
                        convert_operand_to_measure_description(value.operand),
                        convert_operand_to_measure_description(
                            Constant.of(value.index)
                            if isinstance(value.index, int | Sequence)
                            else value.index,
                        ),
                    ],
                ),
            )

        raise TypeError(f"Unexpected operation type: `{type(value)}`.")

    return ConstantMeasure(_value=Constant.of(value))
