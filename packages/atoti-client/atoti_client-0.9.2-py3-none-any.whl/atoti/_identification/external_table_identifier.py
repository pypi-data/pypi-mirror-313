from dataclasses import KW_ONLY
from typing import final

from pydantic.dataclasses import dataclass
from typing_extensions import override

from ._identifier_pydantic_config import IDENTIFIER_PYDANTIC_CONFIG
from .catalog_name import CatalogName
from .identifier import Identifier
from .schema_name import SchemaName
from .table_name import TableName


@final
@dataclass(config=IDENTIFIER_PYDANTIC_CONFIG, frozen=True, order=True)
class ExternalTableIdentifier(Identifier):
    catalog_name: CatalogName
    schema_name: SchemaName
    table_name: TableName
    _: KW_ONLY

    @override
    def __repr__(self) -> str:
        return (
            f"""t[{self.catalog_name, self.schema_name, self.table_name}]"""
            if self.catalog_name
            else f"""t[{self.schema_name, self.table_name}]"""
        )
