from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from typing import Literal, final

from typing_extensions import override

from .._constant import Constant
from .._data_type import DataType, is_primitive_type
from .._identification import HierarchyIdentifier, LevelIdentifier, MeasureIdentifier
from .._java_api import JavaApi
from .._measure_description import MeasureDescription
from .._operation import (
    Condition,
    ConditionComparisonOperatorBound,
    decombine_condition,
)
from .._py4j_utils import to_java_list, to_java_object
from .boolean_measure import BooleanMeasure


def is_object_type(data_type: DataType, /) -> bool:
    return not is_primitive_type(data_type)


@final
@dataclass(eq=False, frozen=True, kw_only=True)
class WhereMeasure(MeasureDescription):
    """A measure that returns the value of other measures based on conditions."""

    _measures_and_conditions: Sequence[
        tuple[MeasureDescription, tuple[MeasureDescription, ...]]
    ]
    _default_measure: MeasureDescription | None

    @override
    def _do_distil(
        self,
        identifier: MeasureIdentifier | None = None,
        /,
        *,
        java_api: JavaApi,
        cube_name: str,
    ) -> MeasureIdentifier:
        underlying_measure_name_to_conditions: dict[
            str,
            tuple[MeasureDescription, ...],
        ] = {}

        for measure, conditions in self._measures_and_conditions:
            underlying_measure_name = measure._distil(
                java_api=java_api,
                cube_name=cube_name,
            ).measure_name
            existing_conditions = underlying_measure_name_to_conditions.get(
                underlying_measure_name,
            )

            match existing_conditions:
                case None:
                    merged_conditions = conditions
                case (BooleanMeasure("or", operands),):
                    # Merge operands to avoid nesting `BooleanMeasure`s and thus prevent a `RecursionError` from being raised when publishing.
                    merged_conditions = (
                        BooleanMeasure(
                            "or",
                            (
                                *operands,
                                BooleanMeasure("and", conditions),
                            ),
                        ),
                    )
                case _:
                    merged_conditions = (
                        BooleanMeasure(
                            "or",
                            (
                                BooleanMeasure("and", existing_conditions),
                                BooleanMeasure("and", conditions),
                            ),
                        ),
                    )

            underlying_measure_name_to_conditions[underlying_measure_name] = (
                merged_conditions
            )

        underlying_default_measure = (
            self._default_measure._distil(
                java_api=java_api,
                cube_name=cube_name,
            ).measure_name
            if self._default_measure is not None
            else None
        )

        return java_api.create_measure(
            identifier,
            "WHERE",
            {
                measure_name: [
                    condition._distil(
                        java_api=java_api,
                        cube_name=cube_name,
                    ).measure_name
                    for condition in conditions
                ]
                for measure_name, conditions in underlying_measure_name_to_conditions.items()
            },
            underlying_default_measure,
            cube_name=cube_name,
        )


FilterCondition = Condition[
    HierarchyIdentifier | LevelIdentifier,
    ConditionComparisonOperatorBound,
    Constant,
    Literal["and"] | None,
]


@final
@dataclass(eq=False, frozen=True, kw_only=True)
class LevelValueFilteredMeasure(MeasureDescription):
    """A measure on a part of the cube filtered on a level value."""

    _underlying_measure: MeasureDescription
    _condition: FilterCondition

    @override
    def _do_distil(
        self,
        identifier: MeasureIdentifier | None = None,
        /,
        *,
        cube_name: str,
        java_api: JavaApi,
    ) -> MeasureIdentifier:
        underlying_name: str = self._underlying_measure._distil(
            java_api=java_api,
            cube_name=cube_name,
        ).measure_name

        (
            comparison_conditions,
            isin_conditions,
            hierarchy_isin_conditions,
        ) = decombine_condition(  # type: ignore[var-annotated]
            self._condition,
            allowed_subject_types=(LevelIdentifier,),
            allowed_combination_operators=("and",),
            allowed_target_types=(Constant,),
            allowed_isin_element_types=(Constant,),
        )[0]

        conditions: list[dict[str, object]] = []

        conditions.extend(
            {
                "level": comparison_condition.subject._java_description,
                "type": "constant",
                "operation": comparison_condition.operator,
                "value": to_java_object(
                    comparison_condition.target.value,
                    gateway=java_api.gateway,
                ),
            }
            for comparison_condition in comparison_conditions
        )

        conditions.extend(
            {
                "level": isin_condition.subject._java_description,
                "type": "constant",
                "operation": "li",
                "value": to_java_list(
                    [element.value for element in isin_condition.elements],
                    gateway=java_api.gateway,
                ),
            }
            for isin_condition in isin_conditions
        )

        conditions.extend(
            {
                "level": LevelIdentifier(
                    hierarchy_isin_condition.subject,
                    hierarchy_isin_condition.level_names[0],
                )._java_description,
                "type": "constant",
                "operation": "hi",
                "value": [
                    {
                        LevelIdentifier(
                            hierarchy_isin_condition.subject,
                            level_name,
                        )._java_description: member.value
                        for level_name, member in zip(
                            hierarchy_isin_condition.level_names,
                            member_path,
                            strict=False,
                        )
                    }
                    for member_path in hierarchy_isin_condition.member_paths
                ],
            }
            for hierarchy_isin_condition in hierarchy_isin_conditions
        )

        # Create the filtered measure and return its name.
        return java_api.create_measure(
            identifier,
            "FILTER",
            underlying_name,
            conditions,
            cube_name=cube_name,
        )
