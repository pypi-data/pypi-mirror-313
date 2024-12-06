from dataclasses import KW_ONLY
from typing import final

from pydantic.dataclasses import dataclass
from typing_extensions import override

from .._graphql_client import ColumnIdentifierInput
from ._identifier_pydantic_config import IDENTIFIER_PYDANTIC_CONFIG
from .column_name import ColumnName
from .identifier import Identifier
from .table_identifier import TableIdentifier


@final
@dataclass(config=IDENTIFIER_PYDANTIC_CONFIG, frozen=True)
class ColumnIdentifier(Identifier):
    table_identifier: TableIdentifier
    column_name: ColumnName
    _: KW_ONLY

    @property
    def _graphql_input(self) -> ColumnIdentifierInput:
        return ColumnIdentifierInput(
            table_identifier=self.table_identifier._graphql_input,
            column_name=self.column_name,
        )

    @override
    def __repr__(self) -> str:
        return f"""{self.table_identifier!r}["{self.column_name}"]"""
