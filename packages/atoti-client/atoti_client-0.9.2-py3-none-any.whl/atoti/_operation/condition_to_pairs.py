from typing import Literal, cast

from .decombine_condition import decombine_condition
from .operation import (
    ComparisonCondition,
    Condition,
    ConditionSubjectT_co,
    ConditionTargetT_co,
)


def condition_to_pairs(
    condition: Condition[
        ConditionSubjectT_co,
        Literal["eq"],
        ConditionTargetT_co,
        Literal["and"] | None,
    ],
    /,
) -> list[tuple[ConditionSubjectT_co, ConditionTargetT_co]]:
    comparison_conditions = cast(
        tuple[
            ComparisonCondition[
                ConditionSubjectT_co,
                Literal["eq"],
                ConditionTargetT_co,
            ],
            ...,
        ],
        decombine_condition(
            condition,
            allowed_comparison_operators=("eq",),
            allowed_combination_operators=("and",),
            allowed_isin_element_types=(),
        )[0][0],
    )
    return [
        (condition.subject, condition.target) for condition in comparison_conditions
    ]
