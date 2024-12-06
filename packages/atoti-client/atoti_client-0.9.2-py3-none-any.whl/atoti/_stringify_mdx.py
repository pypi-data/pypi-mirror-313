# Adapted from https://github.com/activeviam/atoti-ui/blob/eb113a9164ee18443d35ce3bb9e09111c76c4db2/packages/mdx/src/stringify.ts.


from typing_extensions import assert_never

from ._mdx_ast import (
    MdxAst,
    MdxAxis,
    MdxAxisBound,
    MdxCompoundIdentifier,
    MdxFromClause,
    MdxFunction,
    MdxHierarchyCompoundIdentifier,
    MdxIdentifier,
    MdxLevelCompoundIdentifier,
    MdxLiteral,
    MdxMeasureCompoundIdentifier,
    MdxMemberCompoundIdentifier,
    MdxSelect,
    MdxSubSelect,
)


def _escape(value: str, /) -> str:
    return value.replace("]", "]]")


def _quote(*values: str) -> str:
    return ".".join(f"[{_escape(value)}]" for value in values)


def _stringify_axis(axis: MdxAxisBound, /) -> str:
    parts = [
        "NON EMPTY " if axis.non_empty else "",
        stringify_mdx(axis.expression),
    ]

    if axis.properties:
        parts.append(" DIMENSION PROPERTIES ")
        parts.append(
            ", ".join(
                stringify_mdx(axis_property) for axis_property in axis.properties
            ),
        )

    if axis.name != "SLICER":
        parts.append(" ON ")
        parts.append(axis.name)

    return "".join(parts)


def _stringify_compound_identifier(
    compound_identifier: MdxCompoundIdentifier,
    /,
) -> str:
    return ".".join(
        stringify_mdx(identifier) for identifier in compound_identifier.identifiers
    )


def _stringify_from_clause(from_clause: MdxFromClause, /) -> str:
    return f"FROM {_quote(from_clause.cube_name)}"


def _stringify_function(function: MdxFunction, /) -> str:
    if function.syntax == "Braces" or function.syntax == "Parentheses":
        opening_character = function.name[0]
        closing_character = function.name[1]
        return f"{opening_character}{', '.join(stringify_mdx(argument) for argument in function.arguments)}{closing_character}"
    if function.syntax == "Function":
        return f"{function.name}({', '.join(stringify_mdx(argument) for argument in function.arguments)})"
    if function.syntax == "Infix":
        return f" {function.name} ".join(
            stringify_mdx(argument) for argument in function.arguments
        )
    if function.syntax == "Property":
        return f"{stringify_mdx(function.arguments[0])}.{function.name}"
    assert_never(function.syntax)


def _stringify_identifier(identifier: MdxIdentifier, /) -> str:
    return _quote(identifier.value)


def _stringify_literal(literal: MdxLiteral, /) -> str:
    if literal.type == "KEYWORD" or literal.type == "SCALAR":
        return literal.value
    if literal.type == "STRING":
        return f'"{literal.value}"'
    assert_never(literal.type)


def _stringify_select(select: MdxSelect | MdxSubSelect, /) -> str:
    parts = ["SELECT "]

    if select.axes:
        parts.extend(", ".join(stringify_mdx(axis) for axis in select.axes))
        parts.append(" ")

    parts.append(stringify_mdx(select.from_clause))

    if select.slicer_axis:
        parts.append(f" WHERE {stringify_mdx(select.slicer_axis)}")

    return "".join(parts)


def _stringify_sub_select(sub_select: MdxSubSelect, /) -> str:
    return f"FROM ({_stringify_select(sub_select)})"


def stringify_mdx(mdx: MdxAst, /) -> str:  # noqa: PLR0911
    if isinstance(mdx, MdxAxis):
        return _stringify_axis(mdx)
    if isinstance(
        mdx,
        MdxHierarchyCompoundIdentifier
        | MdxLevelCompoundIdentifier
        | MdxMeasureCompoundIdentifier
        | MdxMemberCompoundIdentifier,
    ):
        return _stringify_compound_identifier(mdx)
    if isinstance(mdx, MdxFromClause):
        return _stringify_from_clause(mdx)
    if isinstance(mdx, MdxFunction):
        return _stringify_function(mdx)
    if isinstance(mdx, MdxIdentifier):
        return _stringify_identifier(mdx)
    if isinstance(mdx, MdxLiteral):
        return _stringify_literal(mdx)
    if isinstance(mdx, MdxSelect):
        return _stringify_select(mdx)
    if isinstance(mdx, MdxSubSelect):
        return _stringify_sub_select(mdx)
    assert_never(mdx)
