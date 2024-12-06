# Adapted from https://github.com/activeviam/atoti-ui/blob/eb113a9164ee18443d35ce3bb9e09111c76c4db2/packages/mdx/src/mdx.types.ts.

from __future__ import annotations

from abc import ABC
from collections.abc import Sequence
from dataclasses import field
from typing import Annotated, Generic, Literal, TypeVar, final

from pydantic import AliasChoices, ConfigDict, Discriminator, Field
from pydantic.dataclasses import dataclass
from typing_extensions import Self

from ._collections import FrozenSequence
from ._identification import (
    MEASURES_HIERARCHY_IDENTIFIER,
    HierarchyIdentifier,
    LevelIdentifier,
    MeasureIdentifier,
)
from ._pydantic import (
    PYDANTIC_CONFIG as __PYDANTIC_CONFIG,
    create_camel_case_alias_generator,
)

_PYDANTIC_CONFIG: ConfigDict = {
    **__PYDANTIC_CONFIG,
    "alias_generator": create_camel_case_alias_generator(
        force_aliased_attribute_names={"element_type"},
    ),
    "arbitrary_types_allowed": False,
    "extra": "ignore",
}


@final
@dataclass(config=_PYDANTIC_CONFIG, frozen=True, kw_only=True)
class MdxLiteral:
    element_type: Literal["Literal"] = field(default="Literal", init=False, repr=False)
    type: Literal["KEYWORD", "SCALAR", "STRING"]
    value: str

    @classmethod
    def keyword(cls, value: str, /) -> Self:
        return cls(type="KEYWORD", value=value)

    @classmethod
    def scalar(cls, value: str, /) -> Self:
        return cls(type="SCALAR", value=value)

    @classmethod
    def string(cls, value: str, /) -> Self:
        return cls(type="STRING", value=value)


@final
@dataclass(config=_PYDANTIC_CONFIG, frozen=True, kw_only=True)
class MdxIdentifier:
    element_type: Literal["Identifier"] = field(
        default="Identifier",
        init=False,
        repr=False,
    )
    quoting: str = field(default="QUOTED", init=False, repr=False)
    value: str

    @classmethod
    def of(cls, value: str, /) -> Self:
        return cls(value=value)


@dataclass(config=_PYDANTIC_CONFIG, frozen=True, kw_only=True)
class _AMdxCompoundIdentifier(ABC):
    element_type: Literal["CompoundIdentifier"] = field(
        default="CompoundIdentifier",
        init=False,
        repr=False,
    )
    identifiers: FrozenSequence[MdxIdentifier]


@final
@dataclass(config=_PYDANTIC_CONFIG, frozen=True, kw_only=True)
class MdxHierarchyCompoundIdentifier(_AMdxCompoundIdentifier):
    type: Literal["hierarchy"] = field(default="hierarchy", init=False, repr=False)
    dimension_name: str
    hierarchy_name: str

    @classmethod
    def of(cls, hierarchy_identifier: HierarchyIdentifier, /) -> Self:
        return cls(
            identifiers=[
                MdxIdentifier.of(hierarchy_identifier.dimension_name),
                MdxIdentifier.of(hierarchy_identifier.hierarchy_name),
            ],
            dimension_name=hierarchy_identifier.dimension_name,
            hierarchy_name=hierarchy_identifier.hierarchy_name,
        )


@final
@dataclass(config=_PYDANTIC_CONFIG, frozen=True, kw_only=True)
class MdxLevelCompoundIdentifier(_AMdxCompoundIdentifier):
    type: Literal["level"] = field(default="level", init=False, repr=False)
    dimension_name: str
    hierarchy_name: str
    level_name: str

    @classmethod
    def of(cls, level_identifier: LevelIdentifier, /) -> Self:
        return cls(
            identifiers=[
                MdxIdentifier.of(level_identifier.hierarchy_identifier.dimension_name),
                MdxIdentifier.of(level_identifier.hierarchy_identifier.hierarchy_name),
                MdxIdentifier.of(level_identifier.level_name),
            ],
            dimension_name=level_identifier.hierarchy_identifier.dimension_name,
            hierarchy_name=level_identifier.hierarchy_identifier.hierarchy_name,
            level_name=level_identifier.level_name,
        )


@final
@dataclass(config=_PYDANTIC_CONFIG, frozen=True, kw_only=True)
class MdxMeasureCompoundIdentifier(_AMdxCompoundIdentifier):
    type: Literal["measure"] = field(default="measure", init=False, repr=False)
    measure_name: str

    @classmethod
    def of(cls, measure_identifier: MeasureIdentifier, /) -> Self:
        return cls(
            identifiers=[
                MdxIdentifier.of(MEASURES_HIERARCHY_IDENTIFIER.dimension_name),
                MdxIdentifier.of(measure_identifier.measure_name),
            ],
            measure_name=measure_identifier.measure_name,
        )


@final
@dataclass(config=_PYDANTIC_CONFIG, frozen=True, kw_only=True)
class MdxMemberCompoundIdentifier(_AMdxCompoundIdentifier):
    type: Literal["member"] = field(default="member", init=False, repr=False)
    dimension_name: str
    hierarchy_name: str
    level_name: str
    path: FrozenSequence[str]

    @classmethod
    def of(
        cls,
        *path: str,
        level_identifier: LevelIdentifier,
        hierarchy_first_level_name: str,
    ) -> Self:
        return cls(
            identifiers=[
                MdxIdentifier.of(level_identifier.hierarchy_identifier.dimension_name),
                MdxIdentifier.of(level_identifier.hierarchy_identifier.hierarchy_name),
                MdxIdentifier.of(hierarchy_first_level_name),
                *[MdxIdentifier.of(value) for value in path],
            ],
            dimension_name=level_identifier.hierarchy_identifier.dimension_name,
            hierarchy_name=level_identifier.hierarchy_identifier.hierarchy_name,
            level_name=level_identifier.level_name,
            path=path,
        )


MdxCompoundIdentifier = Annotated[
    MdxMeasureCompoundIdentifier
    | MdxMemberCompoundIdentifier
    | MdxLevelCompoundIdentifier
    | MdxHierarchyCompoundIdentifier,
    Discriminator("type"),
]


@final
@dataclass(config=_PYDANTIC_CONFIG, frozen=True, kw_only=True)
class MdxFunction:
    element_type: Literal["Function"] = field(
        default="Function",
        init=False,
        repr=False,
    )
    arguments: FrozenSequence[MdxExpression]
    name: str
    syntax: Literal["Braces", "Function", "Infix", "Parentheses", "Property"]

    def __post_init__(self) -> None:
        if self.syntax == "Property":
            assert len(self.arguments) == 1

    @classmethod
    def braces(cls, arguments: Sequence[MdxExpression], /) -> Self:
        return cls(arguments=arguments, name=r"{}", syntax="Braces")

    @classmethod
    def function(cls, name: str, arguments: Sequence[MdxExpression], /) -> Self:
        return cls(arguments=arguments, name=name, syntax="Function")

    @classmethod
    def infix(cls, name: str, arguments: Sequence[MdxExpression], /) -> Self:
        return cls(arguments=arguments, name=name, syntax="Infix")

    @classmethod
    def parentheses(cls, arguments: Sequence[MdxExpression], /) -> Self:
        return cls(arguments=arguments, name="()", syntax="Parentheses")

    @classmethod
    def property(cls, name: str, argument: MdxExpression, /) -> Self:
        return cls(arguments=[argument], name=name, syntax="Property")


MdxExpression = Annotated[
    MdxLiteral | MdxIdentifier | MdxCompoundIdentifier | MdxFunction,
    Discriminator("element_type"),
]

ColumnsAxisName = Literal["COLUMNS"]
RowsAxisName = Literal["ROWS"]
RegularAxisName = Literal[ColumnsAxisName, RowsAxisName]
SlicerAxisName = Literal["SLICER"]
AxisName = Literal[RegularAxisName, SlicerAxisName]
AxisNameT_co = TypeVar("AxisNameT_co", bound=AxisName, covariant=True)


@final
@dataclass(config=_PYDANTIC_CONFIG, frozen=True, kw_only=True)
class MdxAxis(Generic[AxisNameT_co]):
    element_type: Literal["Axis"] = field(default="Axis", init=False, repr=False)
    expression: MdxExpression
    name: AxisNameT_co
    properties: FrozenSequence[MdxAst] = ()
    non_empty: bool = False

    def __post_init__(self) -> None:
        if self.name == "SLICER":
            assert not self.non_empty


MdxAxisBound = MdxAxis[AxisName]


@final
@dataclass(config=_PYDANTIC_CONFIG, frozen=True, kw_only=True)
class MdxFromClause:
    element_type: Literal["From"] = field(default="From", init=False, repr=False)
    cube_name: str


@dataclass(config=_PYDANTIC_CONFIG, frozen=True, kw_only=True)
class _AMdxSelect(ABC):
    axes: FrozenSequence[MdxAxis[RegularAxisName]]
    slicer_axis: MdxAxis[SlicerAxisName] | None = None


@final
@dataclass(config=_PYDANTIC_CONFIG, frozen=True, kw_only=True)
class MdxSelect(_AMdxSelect):
    element_type: Literal["Select"] = field(default="Select", init=False, repr=False)
    # Centralizing this attributed in `_AMdxSelect` leads to Pydantic not aliasing it to `from` when serializing.
    from_clause: Annotated[
        MdxSubSelect | MdxFromClause,
        Field(
            validation_alias=AliasChoices("from_clause", "from"),
            serialization_alias="from",
        ),
    ]
    with_clause: FrozenSequence[object] = field(default=(), init=False, repr=False)


@final
@dataclass(config=_PYDANTIC_CONFIG, frozen=True, kw_only=True)
class MdxSubSelect(_AMdxSelect):
    element_type: Literal["SubSelect"] = field(
        default="SubSelect",
        init=False,
        repr=False,
    )
    # Centralizing this attributed in `_AMdxSelect` leads to Pydantic not aliasing it to `from` when serializing.
    from_clause: Annotated[
        MdxSubSelect | MdxFromClause,
        Field(
            validation_alias=AliasChoices("from_clause", "from"),
            serialization_alias="from",
        ),
    ]


MdxAst = Annotated[
    MdxExpression | MdxAxisBound | MdxFromClause | MdxSelect | MdxSubSelect,
    Discriminator("element_type"),
]
