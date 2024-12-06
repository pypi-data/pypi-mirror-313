from collections import defaultdict
from collections.abc import Set as AbstractSet
from itertools import chain, product
from typing import TypeVar, cast

from .._constant import Constant
from .._identification import Identifier
from ._boolean_operator import BOOLEAN_OPERATORS, BooleanOperator
from .comparison_operator import COMPARIONS_OPERATORS, ComparisonOperator
from .hierarchy_isin_condition import HierarchyIsinCondition
from .isin_condition import IsinCondition, IsinConditionElementT_co
from .operation import (
    CombinedCondition,
    ComparisonCondition,
    ConditionBound,
    ConditionSubjectBound,
    ConditionSubjectT_co,
    ConditionTargetT_co,
    Operation,
)

_CombinationOperatorT = TypeVar("_CombinationOperatorT", bound=BooleanOperator)


_ComparisonOperatorT_co = TypeVar(
    "_ComparisonOperatorT_co",
    bound=ComparisonOperator,
    covariant=True,
)


def _check_subject(
    subject: ConditionSubjectBound,
    /,
    *,
    allowed_types: tuple[type[ConditionSubjectT_co], ...],
) -> ConditionSubjectT_co:
    if not isinstance(subject, allowed_types):
        raise TypeError(
            f"Expected the type of the condition's subject to be one of `{tuple(allowed_type.__name__ for allowed_type in allowed_types)}` but got `{type(subject).__name__}`.",
        )
    return subject


def decombine_condition(  # noqa: C901, PLR0912
    condition: ConditionBound,
    /,
    *,
    allowed_subject_types: tuple[
        type[ConditionSubjectT_co],
        ...,
        # Pyright is able to check the default value's type but mypy cannot.
    ] = (  # type: ignore[assignment]
        Identifier,
        Operation,
    ),
    allowed_comparison_operators: tuple[
        _ComparisonOperatorT_co,
        ...,
        # Pyright is able to check the default value's type but mypy cannot.
    ] = COMPARIONS_OPERATORS,  # type: ignore[assignment]
    allowed_target_types: tuple[
        type[ConditionTargetT_co],
        ...,
        # Pyright is able to check the default value's type but mypy cannot.
    ] = (  # type: ignore[assignment]
        type(None),
        Constant,
        Identifier,
        Operation,
    ),
    allowed_combination_operators: tuple[
        _CombinationOperatorT,
        ...,
        # Pyright is able to check the default value's type but mypy cannot.
    ] = BOOLEAN_OPERATORS,  # type: ignore[assignment]
    allowed_isin_element_types: tuple[
        type[IsinConditionElementT_co],
        ...,
        # Pyright is able to check the default value's type but mypy cannot.
    ] = (  # type: ignore[assignment]
        type(None),
        Constant,
    ),
) -> tuple[
    tuple[
        tuple[
            ComparisonCondition[
                ConditionSubjectT_co,
                _ComparisonOperatorT_co,
                ConditionTargetT_co,
            ],
            ...,
        ],
        tuple[IsinCondition[ConditionSubjectT_co, IsinConditionElementT_co], ...],
        tuple[HierarchyIsinCondition, ...],
    ],
    ...,
]:
    """Decombine the passed condition into leave conditions in disjunctive normal form.

    For example: ``c1 & (c2 | c3)`` will return ``((c_1, c_2), (c_1, c_3))``.

    If ``allowed_combination_operators=("and",)`` is passed, the top level tuple will have a single element.

    If ``allowed_isin_element_types=()`` is passed, the tuples containing isin and hierarchy isin conditions will be empty.
    """
    if isinstance(condition, ComparisonCondition):
        subject = _check_subject(condition.subject, allowed_types=allowed_subject_types)

        operator = condition.operator
        if operator not in allowed_comparison_operators:
            raise ValueError(
                f"Expected `{ComparisonCondition.__name__}`'s operator to be one of `{allowed_comparison_operators}` but got `{operator}`.",
            )
        operator = cast(_ComparisonOperatorT_co, operator)

        target = condition.target
        if not isinstance(target, allowed_target_types):
            raise TypeError(
                f"Expected the type of `{ComparisonCondition.__name__}`'s target to be one of `{tuple(allowed_type.__name__ for allowed_type in allowed_target_types)}` but got `{type(target).__name__}`.",
            )

        return (
            (
                (ComparisonCondition(subject, operator, target),),
                (),
                (),
            ),
        )

    if isinstance(condition, IsinCondition):
        if not allowed_isin_element_types:
            raise TypeError(
                f"Expected no `isin` condition but got a `{type(condition).__name__}`.",
            )

        subject = _check_subject(condition.subject, allowed_types=allowed_subject_types)

        elements = condition.elements
        for element in elements:
            if not isinstance(element, allowed_isin_element_types):
                raise TypeError(
                    f"Expected the type of the `{IsinCondition.__name__}`'s elements to be one of `{tuple(allowed_type.__name__ for allowed_type in allowed_isin_element_types)}` but got `{type(element).__name__}`.",
                )
        elements = cast(AbstractSet[IsinConditionElementT_co], elements)

        return (((), (IsinCondition(subject, elements),), ()),)

    if isinstance(condition, HierarchyIsinCondition):
        if not allowed_isin_element_types:
            raise TypeError(
                f"Expected no `isin` condition but got a `{type(condition).__name__}`.",
            )

        return (((), (), (condition,)),)

    if isinstance(condition, CombinedCondition):
        operator = condition.operator

        if not allowed_combination_operators:
            raise ValueError(
                f"Expected single condition but got a `{CombinedCondition.__name__}` using the `{operator}` operator.",
            )

        if operator not in allowed_combination_operators:
            raise ValueError(
                f"Expected `{CombinedCondition.__name__}`'s operator to be one of `{allowed_combination_operators}` but got `{operator}`.",
            )

        first_decombined_conditions, second_decombined_conditions = (
            decombine_condition(
                sub_condition,
                allowed_subject_types=allowed_subject_types,
                allowed_comparison_operators=allowed_comparison_operators,
                allowed_target_types=allowed_target_types,
                allowed_combination_operators=allowed_combination_operators,
                allowed_isin_element_types=allowed_isin_element_types,
            )
            for sub_condition in condition.sub_conditions
        )

        if operator == "or":
            return first_decombined_conditions + second_decombined_conditions

        mixed_first_decombined_conditions, mixed_second_decombined_conditions = (
            [
                comparison_conditions + isin_conditions + hierarchy_isin_conditions
                for comparison_conditions, isin_conditions, hierarchy_isin_conditions in decombined_conditions
            ]
            for decombined_conditions in [
                first_decombined_conditions,
                second_decombined_conditions,
            ]
        )

        decombined_conditions: list[
            tuple[
                tuple[
                    ComparisonCondition[
                        ConditionSubjectT_co,
                        _ComparisonOperatorT_co,
                        ConditionTargetT_co,
                    ],
                    ...,
                ],
                tuple[
                    IsinCondition[ConditionSubjectT_co, IsinConditionElementT_co],
                    ...,
                ],
                tuple[HierarchyIsinCondition, ...],
            ],
        ] = []

        for normalized_conditions in (
            chain(*mixed_decombined_conditions)
            for mixed_decombined_conditions in product(
                mixed_first_decombined_conditions,
                mixed_second_decombined_conditions,
            )
        ):
            type_to_conditions: dict[type[ConditionBound], list[ConditionBound]] = (
                defaultdict(list)
            )

            for normalized_condition in normalized_conditions:
                type_to_conditions[type(normalized_condition)].append(
                    normalized_condition,
                )

            decombined_conditions.append(
                (
                    tuple(
                        cast(
                            list[
                                ComparisonCondition[
                                    ConditionSubjectT_co,
                                    _ComparisonOperatorT_co,
                                    ConditionTargetT_co,
                                ],
                            ],
                            type_to_conditions.get(ComparisonCondition, []),
                        ),
                    ),
                    tuple(
                        cast(
                            list[
                                IsinCondition[
                                    ConditionSubjectT_co,
                                    IsinConditionElementT_co,
                                ]
                            ],
                            type_to_conditions.get(IsinCondition, []),
                        ),
                    ),
                    tuple(
                        cast(
                            list[HierarchyIsinCondition],
                            type_to_conditions.get(HierarchyIsinCondition, []),
                        ),
                    ),
                ),
            )

        return tuple(decombined_conditions)

    raise TypeError(f"Unexpected condition type: `{type(condition).__name__}`.")
