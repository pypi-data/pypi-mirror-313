from __future__ import annotations

import re
from dataclasses import KW_ONLY
from typing import final

from pydantic.dataclasses import dataclass
from typing_extensions import override

from ._data_type import data_type_from_graphql
from ._graphql_client import (
    GetDatabaseSchemaDataModel,
    GetDatabaseSchemaDataModelTablesColumns,
    GetDatabaseSchemaDataModelTablesJoins,
    RelationshipOptionality,
)
from ._mermaid_diagram import MermaidDiagram
from ._pydantic import PYDANTIC_CONFIG as _PYDANTIC_CONFIG

_QUOTE = '"'


def _validate_attribute_word(value: str, /) -> str:
    if (
        re.match(
            # See https://github.com/mermaid-js/mermaid/blob/6e6455632668f5f674ea43bd49ac1a653d232f0c/packages/mermaid/src/diagrams/er/parser/erDiagram.jison#L28C8-L28C42.
            r"[\*A-Za-z_][A-Za-z0-9\-_\[\]\(\)]*",
            value,
        )
        is None
    ):
        raise ValueError(f"Invalid attribute word: `{value}`.")

    return value


def _validate_word(value: str, /) -> str:
    if _QUOTE in value:
        # See https://github.com/mermaid-js/mermaid/blob/6e6455632668f5f674ea43bd49ac1a653d232f0c/packages/mermaid/src/diagrams/er/parser/erDiagram.jison#L21.
        raise ValueError(f"""Unsupported `{_QUOTE}` in `{value}`""")

    return value


def _quote(value: str, /) -> str:
    # See https://github.com/mermaid-js/mermaid/blob/6e6455632668f5f674ea43bd49ac1a653d232f0c/packages/mermaid/src/diagrams/er/parser/erDiagram.jison#L29.
    return f"{_QUOTE}{_validate_word(value)}{_QUOTE}"


def _column_to_attribute(
    column: GetDatabaseSchemaDataModelTablesColumns,
    /,
    *,
    is_key: bool,
) -> str:
    # See https://github.com/mermaid-js/mermaid/blob/6e6455632668f5f674ea43bd49ac1a653d232f0c/packages/mermaid/src/diagrams/er/parser/erDiagram.jison#L26.
    key_attribute = "PK"
    # See https://github.com/mermaid-js/mermaid/blob/6e6455632668f5f674ea43bd49ac1a653d232f0c/packages/mermaid/src/diagrams/er/parser/erDiagram.jison#L127-L132.
    # Mermaid supports a very restricted set of characters in attribute names.
    # See https://github.com/mermaid-js/mermaid/issues/1895.
    # To work around this, the column name is declared in the attribute comment, the column nullability is declared in the attribute type and the column data type is declared in the attribute name.
    return " ".join(
        [
            _validate_attribute_word(
                "nullable" if column.default_value is None else "_",
            ),
            _validate_attribute_word(data_type_from_graphql(column.data_type)),
            *([key_attribute] if is_key else []),
            _quote(column.name),
        ],
    )


def _get_relationship(join: GetDatabaseSchemaDataModelTablesJoins, /) -> str:
    source_cardinality = "}o"

    match join.target_optionality:
        case RelationshipOptionality.MANDATORY:
            target_cardinality = "|{" if join.is_partial else "||"
        case RelationshipOptionality.OPTIONAL:
            target_cardinality = "o{" if join.is_partial else "o|"

    return f"""{source_cardinality}{".." if join.is_partial else "--"}{target_cardinality}"""


def _get_relationship_label(join: GetDatabaseSchemaDataModelTablesJoins, /) -> str:
    def parenthesize(value: str, /) -> str:
        return value if len(join.mapping_items) == 1 else f"({value})"

    return " & ".join(
        parenthesize(
            f"`{_validate_word(item.source.name)}` == `{_validate_word(item.target.name)}`",
        )
        for item in join.mapping_items
    )


def _generate_mermaid_diagram_code(schema: GetDatabaseSchemaDataModel, /) -> str:
    indent = "  "
    lines: list[str] = ["erDiagram"]

    for table in schema.tables:
        lines.append(f"{indent}{_quote(table.name)} {{")

        keys = frozenset({column.name for column in table.primary_index})

        lines.extend(
            f"{indent}{indent}{_column_to_attribute(column, is_key=column.name in keys)}"
            for column in table.columns
        )

        lines.append(f"{indent}}}")

    lines.extend(
        " ".join(
            [
                f"{indent}{_quote(table.name)}",
                _get_relationship(join),
                _quote(join.target.name),
                f": {_quote(_get_relationship_label(join))}",
            ],
        )
        for table in schema.tables
        for join in table.joins
    )

    lines.append("")

    return "\n".join(lines)


@final
@dataclass(config=_PYDANTIC_CONFIG, frozen=True)
class DatabaseSchema(MermaidDiagram):
    value: GetDatabaseSchemaDataModel
    _: KW_ONLY

    @property
    @override
    def _mermaid_diagram_code(self) -> str:
        return _generate_mermaid_diagram_code(self.value)

    @override
    def __repr__(self) -> str:
        return super().__repr__()
