from collections.abc import Sequence
from dataclasses import KW_ONLY, asdict
from pathlib import Path
from typing import final

from pydantic.dataclasses import dataclass
from typing_extensions import override

from .._collections import FrozenMapping, FrozenSequence, frozendict
from .._identification import ColumnName
from .._pydantic import PYDANTIC_CONFIG as _PYDANTIC_CONFIG
from ..client_side_encryption_config import ClientSideEncryptionConfig
from ._split_globfree_absolute_path_and_glob_pattern import (
    split_globfree_absolute_path_and_glob_pattern,
)
from .data_load import DataLoad

_PLUGIN_KEY = "CSV"


@final
@dataclass(config=_PYDANTIC_CONFIG, frozen=True)
class CsvLoad(DataLoad):
    """The description of a CSV file load.

    Example:
        .. doctest::
            :hide:

            >>> directory = getfixture("tmp_path")
            >>> session = getfixture("default_session")

        >>> import csv
        >>> from pathlib import Path
        >>> file_path = directory / "largest-cities.csv"
        >>> with open(file_path, "w") as csv_file:
        ...     writer = csv.writer(csv_file)
        ...     writer.writerows(
        ...         [
        ...             ("city", "area", "country", "population"),
        ...             ("Tokyo", "Kantō", "Japan", 14_094_034),
        ...             ("Johannesburg", "Gauteng", "South Africa", 4_803_262),
        ...             (
        ...                 "Barcelona",
        ...                 "Community of Madrid",
        ...                 "Madrid",
        ...                 3_223_334,
        ...             ),
        ...         ]
        ...     )

        Using :attr:`columns` to drop the :guilabel:`population` column and rename and reorder the remaining ones:

        >>> csv_load = tt.CsvLoad(
        ...     file_path,
        ...     columns={"city": "City", "area": "Region", "country": "Country"},
        ... )
        >>> session.tables.infer_data_types(csv_load)
        {'City': 'String', 'Region': 'String', 'Country': 'String'}

        Creating a table and loading data into it from a headerless CSV file:

        >>> file_path = directory / "largest-cities-headerless.csv"
        >>> with open(file_path, "w") as csv_file:
        ...     writer = csv.writer(csv_file)
        ...     writer.writerows(
        ...         [
        ...             ("Tokyo", "Kantō", "Japan", 14_094_034),
        ...             ("Johannesburg", "Gauteng", "South Africa", 4_803_262),
        ...             (
        ...                 "Madrid",
        ...                 "Community of Madrid",
        ...                 "Spain",
        ...                 3_223_334,
        ...             ),
        ...         ]
        ...     )
        >>> csv_load = tt.CsvLoad(
        ...     file_path,
        ...     columns=["City", "Area", "Country", "Population"],
        ... )
        >>> data_types = session.tables.infer_data_types(csv_load)
        >>> data_types
        {'City': 'String', 'Area': 'String', 'Country': 'String', 'Population': 'int'}
        >>> table = session.create_table(
        ...     "Example",
        ...     data_types=data_types,
        ...     keys={"Country"},
        ... )
        >>> table.load(csv_load)
        >>> table.head().sort_index()
                              City                 Area  Population
        Country
        Japan                Tokyo                Kantō    14094034
        South Africa  Johannesburg              Gauteng     4803262
        Spain               Madrid  Community of Madrid     3223334

    See Also:
        The other :class:`~atoti.data_load.DataLoad` implementations.

    """

    path: Path | str
    """The path to the CSV file to load.

    ``.gz``, ``.tar.gz`` and ``.zip`` files containing compressed CSV(s) are also supported.

    The path can also be a glob pattern (e.g. ``"path/to/directory/*.csv"``).
    """

    _: KW_ONLY

    array_separator: str | None = None
    """The character separating array elements.

    If not ``None``, any field containing this separator will be parsed as an :mod:`~atoti.array`.
    """

    buffer_size_kb: int | None = None
    """:meta private:"""

    client_side_encryption: ClientSideEncryptionConfig | None = None

    columns: FrozenMapping[str, ColumnName] | FrozenSequence[ColumnName] = frozendict()
    """The collection used to name, rename, or filter the CSV file columns.

    * If an empty collection is passed, the CSV file must have a header.
        The CSV column names must follow the :class:`~atoti.Table` column names.
    * If a non empty :class:`~collections.abc.Mapping` is passed, the CSV file must have a header and the mapping keys must be column names of the CSV file.
        Columns of the CSV file absent from the mapping keys will not be loaded.
        The mapping values correspond to the :class:`~atoti.Table` column names.
        The other attributes of this class accepting column names expect to be passed values of this mapping, not keys.
    * If a non empty :class:`~collections.abc.Sequence` is passed, the CSV file must not have a header and the sequence must have as many elements as there are columns in the CSV file.
        The sequence elements correspond to the :class:`~atoti.Table` column names.

    """

    date_patterns: FrozenMapping[ColumnName, str] = frozendict()
    """A column name to `date pattern <https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/time/format/DateTimeFormatter.html>`__ mapping that can be used when the built-in date parsers fail to recognize the formatted dates in the CSV file."""

    encoding: str = "utf-8"
    """The encoding to use to read the CSV file."""

    separator: str | None = ","
    """The character separating the values of each line.

    If ``None``, it will be inferred in a preliminary partial load."""

    parser_thread_count: int | None = None
    """:meta private:"""

    process_quotes: bool | None = True
    """Whether double quotes should be processed to follow the official CSV specification:

    * ``True``:

        Each field may or may not be enclosed in double quotes (however some programs, such as Microsoft Excel, do not use double quotes at all).
        If fields are not enclosed with double quotes, then double quotes may not appear inside the fields.

        * A double quote appearing inside a field must be escaped by preceding it with another double quote.
        * Fields containing line breaks, double quotes, and commas should be enclosed in double-quotes.

    * ``False``: all double-quotes within a field will be treated as any regular character, following Excel's behavior.
        In this mode, it is expected that fields are not enclosed in double quotes.
        It is also not possible to have a line break inside a field.
    * ``None``: the behavior will be inferred in a preliminary partial load.
    """

    @property
    @override
    def _options(self) -> dict[str, object]:
        globfree_absolute_path, glob_pattern = (
            split_globfree_absolute_path_and_glob_pattern(self.path, extension=".csv")
        )
        return {
            "absolutePath": globfree_absolute_path,
            "arraySeparator": self.array_separator,
            "bufferSize": self.buffer_size_kb,
            "clientSideEncryptionConfig": asdict(self.client_side_encryption)
            if self.client_side_encryption is not None
            else None,
            "columns": {} if isinstance(self.columns, Sequence) else self.columns,
            "datePatterns": self.date_patterns,
            "encoding": self.encoding,
            "globPattern": glob_pattern,
            "headers": self.columns if isinstance(self.columns, Sequence) else [],
            "parserThreads": self.parser_thread_count,
            "processQuotes": self.process_quotes,
            "separator": self.separator,
        }

    @property
    @override
    def _plugin_key(self) -> str:
        return _PLUGIN_KEY
