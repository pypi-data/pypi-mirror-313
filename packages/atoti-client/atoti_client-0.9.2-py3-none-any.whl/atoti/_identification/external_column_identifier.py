from dataclasses import KW_ONLY
from typing import final

from pydantic.dataclasses import dataclass
from typing_extensions import override

from ._identifier_pydantic_config import IDENTIFIER_PYDANTIC_CONFIG
from .column_name import ColumnName
from .external_table_identifier import ExternalTableIdentifier
from .identifier import Identifier


@final
@dataclass(config=IDENTIFIER_PYDANTIC_CONFIG, frozen=True)
class ExternalColumnIdentifier(Identifier):
    table_identifier: ExternalTableIdentifier
    column_name: ColumnName
    _: KW_ONLY

    @override
    def __repr__(self) -> str:
        return f"""{self.table_identifier!r}["{self.column_name}"]"""
