from collections.abc import Set as AbstractSet
from dataclasses import KW_ONLY
from typing import Annotated, Literal, NoReturn, final

from pydantic import AfterValidator, Field
from pydantic.dataclasses import dataclass
from typing_extensions import override

from .._collections import FrozenSequence
from .._constant import Constant
from .._identification import (
    HierarchyIdentifier,
    Identifier,
    LevelIdentifier,
    LevelName,
)
from .._pydantic import PYDANTIC_CONFIG
from .combine_conditions import combine_conditions
from .operation import (
    ComparisonCondition,
    Condition,
    ConditionCombinationOperatorBound,
    _validate_constant_target,
)


@final
@dataclass(config=PYDANTIC_CONFIG, frozen=True)
class HierarchyIsinCondition(
    Condition[HierarchyIdentifier, Literal["isin"], Constant, None],
):
    subject: HierarchyIdentifier
    member_paths: Annotated[
        AbstractSet[
            Annotated[
                tuple[
                    Annotated[Constant, AfterValidator(_validate_constant_target)],
                    ...,
                ],
                Field(min_length=1),
            ]
        ],
        Field(min_length=1),
    ]
    _: KW_ONLY
    level_names: Annotated[FrozenSequence[LevelName], Field(min_length=1)]

    def __post_init__(self) -> None:
        for member_path in self.member_paths:
            if len(member_path) > len(self.level_names):
                raise ValueError(
                    f"Member path `{tuple(member.value for member in member_path)}` contains more than {len(self.level_names)} elements which is the number of levels of `{self.subject!r}`.",
                )

    @property
    def normalized(
        self,
    ) -> Condition[
        HierarchyIdentifier | LevelIdentifier,
        Literal["eq", "isin"],
        Constant,
        Literal["and"] | None,
    ]:
        if len(self.member_paths) != 1:
            return self

        return combine_conditions(
            (
                [
                    ComparisonCondition(
                        LevelIdentifier(self.subject, level_name),
                        "eq",
                        member,
                    )
                    for level_name, member in zip(
                        self.level_names,
                        next(iter(self.member_paths)),
                        strict=False,
                    )
                ],
            ),
        )

    @property
    def combined_comparison_condition(
        self,
    ) -> Condition[
        LevelIdentifier,
        Literal["eq"],
        Constant,
        ConditionCombinationOperatorBound,
    ]:
        return combine_conditions(
            [
                [
                    ComparisonCondition(
                        LevelIdentifier(self.subject, level_name),
                        "eq",
                        member,
                    )
                    for level_name, member in zip(
                        self.level_names,
                        member_path,
                        strict=False,
                    )
                ]
                for member_path in sorted(self.member_paths)
            ],
        )

    @property
    @override
    def _identifier_types(self) -> frozenset[type[Identifier]]:
        return frozenset([type(self.subject)])

    @override
    def __invert__(
        self,
    ) -> NoReturn:
        raise RuntimeError(f"A `{type(self).__name__}` cannot be inverted.")
        # It can actually be done using `~hierarchy_isin_condition.combined_comparison_condition` but this changes the type of `subject` which breaks the contract of `Condition.__invert__()`.

    @override
    def __repr__(self) -> str:
        return f"{self.subject!r}.isin{tuple(tuple(member.value for member in member_path) for member_path in sorted(self.member_paths))!r}"
