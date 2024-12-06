from __future__ import annotations

from collections.abc import Mapping, Sequence, Set as AbstractSet
from dataclasses import dataclass, replace
from typing import Literal, final

from typing_extensions import assert_never

from ._collections import frozendict
from ._constant import Constant
from ._cube_discovery import DiscoveryCube
from ._identification import HierarchyIdentifier, LevelIdentifier, MeasureIdentifier
from ._mdx_ast import (
    ColumnsAxisName,
    MdxAxis,
    MdxExpression,
    MdxFromClause,
    MdxFunction,
    MdxHierarchyCompoundIdentifier,
    MdxLevelCompoundIdentifier,
    MdxLiteral,
    MdxMeasureCompoundIdentifier,
    MdxMemberCompoundIdentifier,
    MdxSelect,
    MdxSubSelect,
    RegularAxisName,
    RowsAxisName,
    SlicerAxisName,
)
from ._operation import (
    ComparisonCondition,
    ComparisonOperator,
    HierarchyIsinCondition,
    IsinCondition,
    decombine_condition,
)
from ._query_filter import QueryFilter


def _generate_columns_axis(
    measure_identifiers: Sequence[MeasureIdentifier],
    /,
) -> MdxAxis[ColumnsAxisName]:
    return MdxAxis(
        expression=MdxFunction.braces(
            [
                MdxMeasureCompoundIdentifier.of(measure_identifier)
                for measure_identifier in measure_identifiers
            ],
        ),
        name="COLUMNS",
    )


def _keep_only_deepest_levels(
    level_identifiers: Sequence[LevelIdentifier],
    /,
    *,
    cube: DiscoveryCube,
) -> dict[LevelIdentifier, int]:
    hierarchy_to_max_level_depth: dict[HierarchyIdentifier, int] = {}

    for level_identifier in level_identifiers:
        hierarchy_identifier = level_identifier.hierarchy_identifier
        current_max_level_depth = hierarchy_to_max_level_depth.get(
            hierarchy_identifier,
            -1,
        )
        level_depth = next(
            level_index
            for level_index, level in enumerate(
                cube.name_to_dimension[hierarchy_identifier.dimension_name]
                .name_to_hierarchy[hierarchy_identifier.hierarchy_name]
                .levels,
            )
            if level.name == level_identifier.level_name
        )

        if level_depth > current_max_level_depth:
            hierarchy_to_max_level_depth[hierarchy_identifier] = level_depth

    return {
        LevelIdentifier(
            hierarchy_identifier,
            cube.name_to_dimension[hierarchy_identifier.dimension_name]
            .name_to_hierarchy[hierarchy_identifier.hierarchy_name]
            .levels[depth]
            .name,
        ): depth
        for hierarchy_identifier, depth in hierarchy_to_max_level_depth.items()
    }


def _generate_level_expression(
    level_identifier: LevelIdentifier,
    /,
    *,
    cube: DiscoveryCube,
    include_totals: bool,
    level_depth: int,
) -> MdxExpression:
    hierarchy = cube.name_to_dimension[
        level_identifier.hierarchy_identifier.dimension_name
    ].name_to_hierarchy[level_identifier.hierarchy_identifier.hierarchy_name]

    if not include_totals:
        return MdxFunction.property(
            "Members",
            MdxLevelCompoundIdentifier.of(level_identifier),
        )

    if hierarchy.slicing:
        first_level_identifier = LevelIdentifier(
            level_identifier.hierarchy_identifier,
            hierarchy.levels[0].name,
        )
        member_expression = MdxFunction.property(
            "Members",
            MdxLevelCompoundIdentifier.of(first_level_identifier),
        )
    else:
        member_expression = MdxFunction.braces(
            [
                MdxMemberCompoundIdentifier.of(
                    "AllMember",
                    level_identifier=LevelIdentifier(
                        level_identifier.hierarchy_identifier,
                        hierarchy.levels[0].name,
                    ),
                    hierarchy_first_level_name=hierarchy.levels[0].name,
                ),
            ],
        )

    if level_depth == 0:
        return member_expression

    return MdxFunction.function(
        "Hierarchize",
        [
            MdxFunction.function(
                "Descendants",
                [
                    member_expression,
                    MdxLiteral.scalar(str(level_depth)),
                    MdxLiteral.keyword("SELF_AND_BEFORE"),
                ],
            ),
        ],
    )


def _generate_rows_axis(
    level_identifiers: Mapping[LevelIdentifier, int],
    /,
    *,
    cube: DiscoveryCube,
    include_totals: bool,
    non_empty: bool,
) -> MdxAxis[RowsAxisName]:
    expression: MdxExpression

    if len(level_identifiers) == 1:
        level_identifier, level_depth = next(iter(level_identifiers.items()))
        expression = _generate_level_expression(
            level_identifier,
            cube=cube,
            include_totals=include_totals,
            level_depth=level_depth,
        )
    else:
        expression = MdxFunction.function(
            "Crossjoin",
            [
                _generate_level_expression(
                    level_identifier,
                    cube=cube,
                    include_totals=include_totals,
                    level_depth=level_depth,
                )
                for level_identifier, level_depth in level_identifiers.items()
            ],
        )

    # Adapted from https://github.com/activeviam/atoti-ui/blob/fd835ae09f2505d5a88a4068208013c092329e55/packages/mdx/src/ensureChildrenCardinalityInMemberProperties.tsx#L18.
    multi_level_hierarchy_identifiers = {
        HierarchyIdentifier(dimension.name, hierarchy.name)
        for dimension in cube.dimensions
        for hierarchy in dimension.hierarchies
        if len(hierarchy.levels) > (1 if hierarchy.slicing else 2)
    }
    has_at_least_one_multi_level_hierarchy = any(
        level_identifier.hierarchy_identifier in multi_level_hierarchy_identifiers
        for level_identifier in level_identifiers
    )
    properties = (
        (MdxLiteral.keyword("CHILDREN_CARDINALITY"),)
        if has_at_least_one_multi_level_hierarchy
        else ()
    )

    return MdxAxis(
        expression=expression,
        name="ROWS",
        non_empty=non_empty,
        properties=properties,
    )


def _is_hierarchy_shallowest_level(
    level_identifier: LevelIdentifier,
    /,
    *,
    cube: DiscoveryCube,
) -> bool:
    shallowest_level = next(
        level
        for level in cube.name_to_dimension[
            level_identifier.hierarchy_identifier.dimension_name
        ]
        .name_to_hierarchy[level_identifier.hierarchy_identifier.hierarchy_name]
        .levels
        if level.type != "ALL"
    )
    return level_identifier.level_name == shallowest_level.name


@final
@dataclass(frozen=True, kw_only=True)
class _HierarchyFilter:
    member_paths: AbstractSet[tuple[Constant, ...]]
    exclusion: bool = False

    def __and__(self, other: _HierarchyFilter, /) -> _HierarchyFilter:
        if not (self.exclusion and other.exclusion):
            raise ValueError("Only exclusion filters can be combined.")

        return _HierarchyFilter(
            exclusion=True,
            member_paths=self.member_paths | other.member_paths,
        )


def _process_conditions(
    *,
    comparison_conditions: Sequence[
        ComparisonCondition[LevelIdentifier, ComparisonOperator, Constant]
    ],
    cube: DiscoveryCube,
    hierarchy_isin_conditions: Sequence[HierarchyIsinCondition],
    isin_conditions: Sequence[IsinCondition[LevelIdentifier, Constant]],
    scenario_name: str | None,
) -> tuple[
    list[
        ComparisonCondition[LevelIdentifier, ComparisonOperator, Constant]
        | IsinCondition[LevelIdentifier, Constant]
    ],
    dict[HierarchyIdentifier, _HierarchyFilter],
]:
    deep_level_conditions: list[
        ComparisonCondition[LevelIdentifier, ComparisonOperator, Constant]
        | IsinCondition[LevelIdentifier, Constant]
    ] = []
    hierarchy_identifier_to_filter: dict[HierarchyIdentifier, _HierarchyFilter] = {}

    def add_hierarchy_filter(
        hierarchy_filter: _HierarchyFilter,
        /,
        *,
        hierarchy_identifier: HierarchyIdentifier,
    ) -> None:
        existing_filter = hierarchy_identifier_to_filter.get(hierarchy_identifier)

        hierarchy_identifier_to_filter[hierarchy_identifier] = (
            existing_filter & hierarchy_filter if existing_filter else hierarchy_filter
        )

    for comparison_condition in comparison_conditions:
        if _is_hierarchy_shallowest_level(comparison_condition.subject, cube=cube) and (
            comparison_condition.operator == "eq"
            or comparison_condition.operator == "ne"
        ):
            add_hierarchy_filter(
                _HierarchyFilter(
                    exclusion=comparison_condition.operator == "ne",
                    member_paths={(comparison_condition.target,)},
                ),
                hierarchy_identifier=comparison_condition.subject.hierarchy_identifier,
            )
        else:
            deep_level_conditions.append(comparison_condition)

    for isin_condition in isin_conditions:
        if _is_hierarchy_shallowest_level(isin_condition.subject, cube=cube):
            add_hierarchy_filter(
                _HierarchyFilter(
                    member_paths={(member,) for member in isin_condition.elements},
                ),
                hierarchy_identifier=isin_condition.subject.hierarchy_identifier,
            )
        else:
            deep_level_conditions.append(isin_condition)

    for hierarchy_isin_condition in hierarchy_isin_conditions:
        add_hierarchy_filter(
            _HierarchyFilter(
                member_paths=hierarchy_isin_condition.member_paths,
            ),
            hierarchy_identifier=hierarchy_isin_condition.subject,
        )

    if scenario_name is not None:
        hierarchy_identifier_to_filter[HierarchyIdentifier("Epoch", "Epoch")] = (
            _HierarchyFilter(member_paths={(Constant.of(scenario_name),)})
        )

    return (deep_level_conditions, hierarchy_identifier_to_filter)


_CONDITION_COMPARISON_OPERATOR_TO_MDX_OPERATOR: Mapping[ComparisonOperator, str] = (
    frozendict({"eq": "=", "ge": ">=", "gt": ">", "le": "<=", "lt": "<", "ne": "<>"})
)


def _constant_to_mdx_literal(constant: Constant, /) -> MdxLiteral:
    json_value = constant._legacy_value_json

    if isinstance(json_value, bool):
        return MdxLiteral.scalar("TRUE" if json_value else "FALSE")
    if isinstance(json_value, float | int):
        return MdxLiteral.scalar(str(json_value))
    if isinstance(json_value, str):
        return MdxLiteral.string(json_value)

    assert_never(json_value)


def _generate_level_filter_expression(
    condition: ComparisonCondition[LevelIdentifier, ComparisonOperator, Constant]
    | IsinCondition[LevelIdentifier, Constant],
) -> MdxExpression:
    current_member_name_expression = MdxFunction.property(
        "MEMBER_VALUE",
        MdxFunction.property(
            "CurrentMember",
            MdxHierarchyCompoundIdentifier.of(condition.subject.hierarchy_identifier),
        ),
    )
    logical_expression: MdxExpression

    if isinstance(condition, ComparisonCondition):
        logical_expression = MdxFunction.infix(
            _CONDITION_COMPARISON_OPERATOR_TO_MDX_OPERATOR[condition.operator],
            [
                current_member_name_expression,
                _constant_to_mdx_literal(condition.target),
            ],
        )
    elif isinstance(condition, IsinCondition):
        logical_expression = MdxFunction.infix(
            "OR",
            [
                MdxFunction.infix(
                    _CONDITION_COMPARISON_OPERATOR_TO_MDX_OPERATOR["eq"],
                    [
                        current_member_name_expression,
                        _constant_to_mdx_literal(element),
                    ],
                )
                for element in sorted(condition.elements)
            ],
        )
    else:
        assert_never(condition)

    return MdxFunction.function(
        "Filter",
        [
            MdxFunction.property(
                "Members",
                MdxLevelCompoundIdentifier.of(condition.subject),
            ),
            logical_expression,
        ],
    )


def _generate_member_compound_identifier(
    member_path: Sequence[Constant],
    /,
    *,
    cube: DiscoveryCube,
    hierarchy_identifier: HierarchyIdentifier,
) -> MdxMemberCompoundIdentifier:
    hierarchy = cube.name_to_dimension[
        hierarchy_identifier.dimension_name
    ].name_to_hierarchy[hierarchy_identifier.hierarchy_name]
    level_index = len(member_path) - 1 if hierarchy.slicing else len(member_path)

    return MdxMemberCompoundIdentifier.of(
        *([] if hierarchy.slicing else ["AllMember"]),
        *(str(member._legacy_value_json) for member in member_path),
        level_identifier=LevelIdentifier(
            hierarchy_identifier,
            level_name=hierarchy.levels[level_index].name,
        ),
        hierarchy_first_level_name=hierarchy.levels[0].name,
    )


_FilterClass = Literal["slicer", "subselect"]


# Adapted from https://github.com/activeviam/atoti-ui/blob/cf8f9aa102ab8eaa88ac1e11f036d56b2e4ca7b6/packages/mdx/src/internal/_getFilterClasses.ts.
def _generate_hierarchy_filter_expression_and_class(
    hierarchy_filter: _HierarchyFilter,
    /,
    *,
    cube: DiscoveryCube,
    hierarchy_identifier: HierarchyIdentifier,
    hierarchy_on_regular_axis: bool,
) -> tuple[MdxExpression, _FilterClass]:
    compound_identifiers = [
        _generate_member_compound_identifier(
            member_path,
            cube=cube,
            hierarchy_identifier=hierarchy_identifier,
        )
        for member_path in sorted(hierarchy_filter.member_paths)
    ]

    expression: MdxExpression = (
        compound_identifiers[0]
        if len(compound_identifiers) == 1
        else MdxFunction.braces(compound_identifiers)
    )

    filter_class: _FilterClass = "subselect"

    if hierarchy_filter.exclusion:
        expression = MdxFunction.function(
            "Except",
            [
                MdxFunction.property(
                    "Members",
                    MdxHierarchyCompoundIdentifier.of(hierarchy_identifier),
                ),
                expression,
            ],
        )
    elif not hierarchy_on_regular_axis and len(hierarchy_filter.member_paths) == 1:
        filter_class = "slicer"

    return expression, filter_class


def _create_slicer_axis(
    slicer_expressions: Sequence[MdxExpression],
    /,
) -> MdxAxis[SlicerAxisName] | None:
    if not slicer_expressions:
        return None

    return MdxAxis(
        expression=slicer_expressions[0]
        if len(slicer_expressions) == 1
        else MdxFunction.parentheses(slicer_expressions),
        name="SLICER",
    )


# Adapted from https://github.com/activeviam/atoti-ui/blob/cf8f9aa102ab8eaa88ac1e11f036d56b2e4ca7b6/packages/mdx/src/internal/_setFiltersWithClasses.ts.
def _add_filters(
    select: MdxSelect,
    filter_expression_to_class: Mapping[MdxExpression, _FilterClass],
    /,
) -> MdxSelect:
    slicer_expressions: list[MdxExpression] = []

    for filter_expression, filter_class in filter_expression_to_class.items():
        if filter_class == "slicer":
            slicer_expressions.append(filter_expression)
        elif filter_class == "subselect":
            select = replace(
                select,
                from_clause=MdxSubSelect(
                    axes=[MdxAxis(expression=filter_expression, name="COLUMNS")],
                    from_clause=select.from_clause,
                    slicer_axis=_create_slicer_axis(slicer_expressions),
                ),
            )
        else:
            assert_never(filter_class)

    return replace(
        select,
        slicer_axis=_create_slicer_axis(slicer_expressions),
    )


def _generate_mdx_with_decombined_conditions(
    *,
    comparison_conditions: Sequence[
        ComparisonCondition[LevelIdentifier, ComparisonOperator, Constant]
    ],
    cube: DiscoveryCube,
    hierarchy_isin_conditions: Sequence[HierarchyIsinCondition],
    include_empty_rows: bool,
    include_totals: bool,
    isin_conditions: Sequence[IsinCondition[LevelIdentifier, Constant]],
    level_identifiers: Sequence[LevelIdentifier],
    measure_identifiers: Sequence[MeasureIdentifier],
    scenario_name: str | None,
) -> MdxSelect:
    axes: list[MdxAxis[RegularAxisName]] = [_generate_columns_axis(measure_identifiers)]

    deepest_levels = _keep_only_deepest_levels(level_identifiers, cube=cube)
    if deepest_levels:
        axes.append(
            _generate_rows_axis(
                deepest_levels,
                cube=cube,
                include_totals=include_totals,
                non_empty=not include_empty_rows,
            ),
        )

    (
        deep_level_conditions,
        hierarchy_identifier_to_filter,
    ) = _process_conditions(
        comparison_conditions=comparison_conditions,
        cube=cube,
        hierarchy_isin_conditions=hierarchy_isin_conditions,
        isin_conditions=isin_conditions,
        scenario_name=scenario_name,
    )

    filter_expression_to_class: dict[MdxExpression, _FilterClass] = {
        **{
            _generate_level_filter_expression(condition): "subselect"
            for condition in deep_level_conditions
        },
        **dict(
            _generate_hierarchy_filter_expression_and_class(
                hierarchy_filter,
                cube=cube,
                hierarchy_identifier=hierarchy_identifier,
                hierarchy_on_regular_axis=any(
                    level_identifier.hierarchy_identifier == hierarchy_identifier
                    for level_identifier in deepest_levels
                ),
            )
            for hierarchy_identifier, hierarchy_filter in hierarchy_identifier_to_filter.items()
        ),
    }

    mdx_select = MdxSelect(axes=axes, from_clause=MdxFromClause(cube_name=cube.name))

    return _add_filters(mdx_select, filter_expression_to_class)


def generate_mdx(
    *,
    cube: DiscoveryCube,
    filter: QueryFilter | None = None,  # noqa: A002
    include_empty_rows: bool = False,
    include_totals: bool = False,
    level_identifiers: Sequence[LevelIdentifier] = (),
    measure_identifiers: Sequence[MeasureIdentifier] = (),
    scenario: str | None = None,
) -> MdxSelect:
    comparison_conditions, isin_conditions, hierarchy_isin_conditions = (
        ((), (), ())  # type: ignore[var-annotated]
        if filter is None
        else decombine_condition(
            filter,
            allowed_subject_types=(LevelIdentifier,),
            allowed_target_types=(Constant,),
            allowed_combination_operators=("and",),
            allowed_isin_element_types=(Constant,),
        )[0]
    )

    return _generate_mdx_with_decombined_conditions(
        comparison_conditions=comparison_conditions,
        cube=cube,
        hierarchy_isin_conditions=hierarchy_isin_conditions,
        include_empty_rows=include_empty_rows,
        include_totals=include_totals,
        isin_conditions=isin_conditions,
        level_identifiers=level_identifiers,
        measure_identifiers=measure_identifiers,
        scenario_name=scenario,
    )
