from typing import TypeAlias

from .catalog_name import CatalogName
from .schema_name import SchemaName
from .table_name import TableName

ExternalTableKey: TypeAlias = (
    TableName | tuple[SchemaName, TableName] | tuple[CatalogName, SchemaName, TableName]
)
