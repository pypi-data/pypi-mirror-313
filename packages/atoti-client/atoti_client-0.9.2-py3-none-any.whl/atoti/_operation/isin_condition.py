from collections.abc import Set as AbstractSet
from dataclasses import KW_ONLY
from typing import Annotated, Literal, TypeVar, final

from pydantic import AfterValidator, Field
from pydantic.dataclasses import dataclass
from typing_extensions import override

from .._constant import Constant
from .._identification import Identifier
from .._pydantic import PYDANTIC_CONFIG
from .combine_conditions import combine_conditions
from .operation import (
    ComparisonCondition,
    Condition,
    ConditionCombinationOperatorBound,
    ConditionComparisonOperatorBound,
    ConditionSubjectT_co,
    _validate_condition_subject,
    _validate_constant_target,
)

IsinConditionElementBound = Constant | None

IsinConditionElementT_co = TypeVar(
    "IsinConditionElementT_co",
    bound=IsinConditionElementBound,
    covariant=True,
)


def _validate_element(
    element: IsinConditionElementBound,
    /,
) -> IsinConditionElementBound:
    return element if element is None else _validate_constant_target(element)


@final
@dataclass(config=PYDANTIC_CONFIG, frozen=True)
class IsinCondition(
    Condition[ConditionSubjectT_co, Literal["isin"], IsinConditionElementT_co, None],
):
    subject: Annotated[
        ConditionSubjectT_co,
        AfterValidator(_validate_condition_subject),
    ]
    elements: Annotated[
        AbstractSet[
            Annotated[IsinConditionElementT_co, AfterValidator(_validate_element)]
        ],
        Field(min_length=1),
    ]
    _: KW_ONLY

    @property
    def sorted_elements(self) -> tuple[IsinConditionElementT_co, ...]:
        return (
            # Collections containing `None` cannot be sorted.
            # If `None` is in the elements it's added at the head of the tuple.
            # The remaining non-`None` elements are sorted and inserted after.
            *([None] if None in self.elements else []),  # type: ignore[arg-type] # pyright: ignore[reportReturnType]
            *sorted(element for element in self.elements if element is not None),  # type: ignore[type-var]
        )

    @property
    def normalized(
        self,
    ) -> Condition[
        ConditionSubjectT_co,
        Literal["eq", "isin"],
        IsinConditionElementT_co,
        None,
    ]:
        if len(self.elements) != 1:
            return self

        return ComparisonCondition(self.subject, "eq", next(iter(self.elements)))

    @property
    def combined_comparison_condition(
        self,
    ) -> Condition[
        ConditionSubjectT_co,
        Literal["eq"],
        IsinConditionElementT_co,
        Literal["or"] | None,
    ]:
        return combine_conditions(
            [
                (ComparisonCondition(self.subject, "eq", element),)
                for element in self.sorted_elements
            ],
        )

    @property
    @override
    def _identifier_types(self) -> frozenset[type[Identifier]]:
        return self._get_identifier_types(self.subject)

    @override
    def __invert__(
        self,
    ) -> Condition[
        ConditionSubjectT_co,
        ConditionComparisonOperatorBound,
        IsinConditionElementT_co,
        ConditionCombinationOperatorBound,
    ]:
        return ~self.combined_comparison_condition

    @override
    def __repr__(self) -> str:
        return f"{self.subject!r}.isin{tuple(element.value if isinstance(element, Constant) else element for element in self.sorted_elements)!r}"


IsinConditionBound = IsinCondition[Identifier, Constant | None]
