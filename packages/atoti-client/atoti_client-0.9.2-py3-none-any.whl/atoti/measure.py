from __future__ import annotations

from typing import Final, Literal, final

from typing_extensions import override

from ._data_type import DataType
from ._identification import CubeIdentifier, MeasureIdentifier
from ._java_api import JavaApi
from ._live_extension_unavailable_error import LiveExtensionUnavailableError
from ._operation import ComparisonCondition, Condition, OperandConvertibleWithIdentifier


@final
class Measure(OperandConvertibleWithIdentifier[MeasureIdentifier]):
    """A measure is a mostly-numeric data value, computed on demand for aggregation purposes.

    Example:
        .. doctest::
            :hide:

            >>> session = getfixture("default_session")

        Copying a measure does not copy its attributes:

        >>> table = session.create_table("Example", data_types={"ID": "String"})
        >>> cube = session.create_cube(table)
        >>> m = cube.measures
        >>> m["Original"] = 1
        >>> m["Original"].description = "Test description"
        >>> m["Original"].folder = "Test folder"
        >>> m["Original"].formatter = "INT[test: #,###]"
        >>> m["Original"].visible = False
        >>> m["Copy"] = m["Original"]
        >>> print(m["Copy"].description)
        None
        >>> print(m["Copy"].folder)
        None
        >>> m["Copy"].formatter
        'INT[#,###]'
        >>> m["Copy"].visible
        True

        Redefining a measure resets its attributes:

        >>> m["Original"] = 2
        >>> print(m["Original"].description)
        None
        >>> print(m["Original"].folder)
        None
        >>> m["Original"].formatter
        'INT[#,###]'
        >>> m["Original"].visible
        True

    See Also:
        :class:`~atoti.measures.Measures` to define one.
    """

    def __init__(
        self,
        identifier: MeasureIdentifier,
        /,
        *,
        cube_identifier: CubeIdentifier,
        data_type: DataType,
        description: str | None,
        folder: str | None,
        formatter: str | None,
        java_api: JavaApi | None,
        visible: bool,
    ) -> None:
        self._cube_identifier: Final = cube_identifier
        self._data_type: Final = data_type
        self._description = description
        self._folder = folder
        self._formatter = formatter
        self.__identifier: Final = identifier
        self.__java_api: Final = java_api
        self._visible = visible

    @property
    def data_type(self) -> DataType:
        """Type of the values the measure evaluates to."""
        return self._data_type

    @property
    def description(self) -> str | None:
        """Description of the measure.

        Example:
            .. doctest::
                :hide:

                >>> session = getfixture("default_session")

            >>> df = pd.DataFrame(
            ...     columns=["Product", "Price"],
            ...     data=[
            ...         ("phone", 560),
            ...         ("headset", 80),
            ...         ("watch", 250),
            ...     ],
            ... )
            >>> table = session.read_pandas(df, keys={"Product"}, table_name="Example")
            >>> cube = session.create_cube(table)
            >>> m = cube.measures
            >>> print(m["Price.SUM"].description)
            None
            >>> m["Price.SUM"].description = "The sum of the price"
            >>> m["Price.SUM"].description
            'The sum of the price'
            >>> del m["Price.SUM"].description
            >>> print(m["Price.SUM"].description)
            None

        """
        return self._description

    @description.setter
    def description(self, value: str) -> None:
        self._set_description(value)

    @description.deleter
    def description(self) -> None:
        self._set_description(None)

    def _set_description(self, value: str | None) -> None:
        self._description = value
        self._java_api.set_measure_description(
            self._identifier,
            value,
            cube_name=self._cube_identifier.cube_name,
        )
        self._java_api.publish_measures(self._cube_identifier.cube_name)

    @property
    def folder(self) -> str | None:
        """Folder of the measure.

        Folders can be used to group measures in the :guilabel:`Data model` UI component.

        Example:
            .. doctest::
                :hide:

                >>> session = getfixture("default_session")

            >>> df = pd.DataFrame(
            ...     columns=["Product", "Price"],
            ...     data=[
            ...         ("phone", 600.0),
            ...         ("headset", 80.0),
            ...         ("watch", 250.0),
            ...     ],
            ... )
            >>> table = session.read_pandas(df, keys={"Product"}, table_name="Example")
            >>> cube = session.create_cube(table)
            >>> m = cube.measures
            >>> print(m["Price.SUM"].folder)
            None
            >>> m["Price.SUM"].folder = "Prices"
            >>> m["Price.SUM"].folder
            'Prices'
            >>> del m["Price.SUM"].folder
            >>> print(m["Price.SUM"].folder)
            None

        """
        return self._folder

    @folder.setter
    def folder(self, value: str) -> None:
        self._set_folder(value)

    @folder.deleter
    def folder(self) -> None:
        self._set_folder(None)

    def _set_folder(self, value: str | None) -> None:
        self._folder = value
        self._java_api.set_measure_folder(
            self._identifier,
            value,
            cube_name=self._cube_identifier.cube_name,
        )
        self._java_api.publish_measures(self._cube_identifier.cube_name)

    @property
    def formatter(self) -> str | None:
        """Formatter of the measure.

        Note:
            The formatter only impacts how the measure is displayed, derived measures will still be computed from unformatted value.
            To round a measure, use :func:`atoti.math.round` instead.

        Example:
            .. doctest::
                :hide:

                >>> session = getfixture("default_session")

            >>> df = pd.DataFrame(
            ...     columns=["Product", "Price", "Quantity"],
            ...     data=[
            ...         ("phone", 559.99, 2),
            ...         ("headset", 79.99, 4),
            ...         ("watch", 249.99, 3),
            ...     ],
            ... )
            >>> table = session.read_pandas(df, keys={"Product"}, table_name="Example")
            >>> cube = session.create_cube(table)
            >>> h, l, m = cube.hierarchies, cube.levels, cube.measures
            >>> m["contributors.COUNT"].formatter
            'INT[#,###]'
            >>> m["contributors.COUNT"].formatter = "INT[count: #,###]"
            >>> m["contributors.COUNT"].formatter
            'INT[count: #,###]'
            >>> m["Price.SUM"].formatter
            'DOUBLE[#,###.00]'
            >>> m["Price.SUM"].formatter = "DOUBLE[$#,##0.00]"  # Add $ symbol
            >>> m["Ratio of sales"] = m["Price.SUM"] / tt.total(
            ...     m["Price.SUM"], h["Product"]
            ... )
            >>> m["Ratio of sales"].formatter
            'DOUBLE[#,###.00]'
            >>> m["Ratio of sales"].formatter = "DOUBLE[0.00%]"  # Percentage
            >>> m["Turnover in dollars"] = tt.agg.sum(
            ...     table["Price"] * table["Quantity"],
            ... )
            >>> m["Turnover in dollars"].formatter
            'DOUBLE[#,###.00]'
            >>> m["Turnover in dollars"].formatter = "DOUBLE[#,###]"  # Without decimals
            >>> cube.query(
            ...     m["contributors.COUNT"],
            ...     m["Price.SUM"],
            ...     m["Ratio of sales"],
            ...     m["Turnover in dollars"],
            ...     levels=[l["Product"]],
            ... )
                    contributors.COUNT Price.SUM Ratio of sales Turnover in dollars
            Product
            headset           count: 1    $79.99          8.99%                 320
            phone             count: 1   $559.99         62.92%               1,120
            watch             count: 1   $249.99         28.09%                 750

        The spec for the pattern between the ``DATE`` or ``DOUBLE``'s brackets is the one from `Microsoft Analysis Services <https://docs.microsoft.com/en-us/analysis-services/multidimensional-models/mdx/mdx-cell-properties-format-string-contents?view=asallproducts-allversions>`__.

        There is an extra formatter for array measures: ``ARRAY['|';1:3]`` where ``|`` is the separator used to join the elements of the ``1:3`` slice.
        """
        return self._formatter

    @formatter.setter
    def formatter(self, value: str) -> None:
        self._formatter = value
        self._java_api.set_measure_formatter(
            self._identifier,
            value,
            cube_name=self._cube_identifier.cube_name,
        )
        self._java_api.publish_measures(self._cube_identifier.cube_name)

    @property
    @override
    def _identifier(self) -> MeasureIdentifier:
        return self.__identifier

    @override
    def isnull(self) -> Condition[MeasureIdentifier, Literal["eq"], None, None]:
        """Return a condition evaluating to ``True`` if the measure evalutes to ``None`` and ``False`` otherwise.

        Use ``~measure.isnull()`` for the opposite behavior.

        Example:
            .. doctest::
                :hide:

                >>> session = getfixture("default_session")

            >>> df = pd.DataFrame(
            ...     columns=["Country", "City", "Price"],
            ...     data=[
            ...         ("France", "Paris", 200.0),
            ...         ("Germany", "Berlin", None),
            ...     ],
            ... )
            >>> table = session.read_pandas(df, table_name="Example")
            >>> cube = session.create_cube(table)
            >>> l, m = cube.levels, cube.measures
            >>> m["Price.isnull"] = m["Price.SUM"].isnull()
            >>> m["Price.notnull"] = ~m["Price.SUM"].isnull()
            >>> cube.query(
            ...     m["Price.isnull"],
            ...     m["Price.notnull"],
            ...     levels=[l["Country"]],
            ... )
                    Price.isnull Price.notnull
            Country
            France         False          True
            Germany         True         False

        """
        return ComparisonCondition(self._operation_operand, "eq", None)

    @property
    def _java_api(self) -> JavaApi:
        if self.__java_api is None:
            raise LiveExtensionUnavailableError
        return self.__java_api

    @property
    def name(self) -> str:
        """Name of the measure."""
        return self._identifier.measure_name

    @property
    @override
    def _operation_operand(self) -> MeasureIdentifier:
        return self._identifier

    @property
    def visible(self) -> bool:
        """Whether the measure is visible or not.

        Example:
            .. doctest::
                :hide:

                >>> session = getfixture("default_session")

            >>> df = pd.DataFrame(
            ...     columns=["Product", "Price"],
            ...     data=[
            ...         ("phone", 560),
            ...         ("headset", 80),
            ...         ("watch", 250),
            ...     ],
            ... )
            >>> table = session.read_pandas(df, keys={"Product"}, table_name="Example")
            >>> cube = session.create_cube(table)
            >>> m = cube.measures
            >>> m["Price.SUM"].visible
            True
            >>> m["Price.SUM"].visible = False
            >>> m["Price.SUM"].visible
            False
            >>> m["contributors.COUNT"].visible
            True
            >>> m["contributors.COUNT"].visible = False
            >>> m["contributors.COUNT"].visible
            False
        """
        return self._visible

    @visible.setter
    def visible(self, value: bool) -> None:
        self._visible = value
        self._java_api.set_measure_visibility(
            self._identifier,
            value,
            cube_name=self._cube_identifier.cube_name,
        )
        self._java_api.publish_measures(self._cube_identifier.cube_name)
