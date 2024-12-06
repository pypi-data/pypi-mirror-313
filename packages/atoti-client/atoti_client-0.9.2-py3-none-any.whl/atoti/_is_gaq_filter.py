from collections.abc import Collection

from typing_extensions import TypeIs

from ._constant import Constant
from ._gaq_filter import GaqFilter
from ._identification import LevelIdentifier
from ._operation import ComparisonOperator, decombine_condition
from ._query_filter import QueryFilter

_SUPPORTED_COMPARISON_OPERATORS: Collection[ComparisonOperator] = frozenset(
    {"eq", "ne"},
)
_SUPPORTED_TARGET_TYPES = (int, float, str)


def is_gaq_filter(
    filter: QueryFilter,  # noqa: A002
    /,
) -> TypeIs[GaqFilter]:
    comparison_conditions, level_isin_conditions, hierarchy_isin_conditions = (
        decombine_condition(  # type: ignore[var-annotated]
            filter,
            allowed_subject_types=(LevelIdentifier,),
            allowed_combination_operators=("and",),
            allowed_target_types=(Constant,),
        )[0]
    )
    return (
        all(
            condition.operator in _SUPPORTED_COMPARISON_OPERATORS
            and isinstance(condition.target.value, _SUPPORTED_TARGET_TYPES)
            for condition in comparison_conditions
        )
        and all(
            element is not None and isinstance(element.value, _SUPPORTED_TARGET_TYPES)
            for condition in level_isin_conditions
            for element in condition.elements
        )
        and not hierarchy_isin_conditions
    )
