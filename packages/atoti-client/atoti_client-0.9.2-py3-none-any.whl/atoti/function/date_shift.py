from __future__ import annotations

from typing import Literal

from .._data_type import is_temporal_type
from .._measure.date_shift import DateShift
from .._measure_convertible import VariableMeasureConvertible
from .._measure_description import MeasureDescription, convert_to_measure_description
from ..hierarchy import Hierarchy

_DateShiftMethod = Literal["exact", "previous", "next", "interpolate"]


def date_shift(
    measure: VariableMeasureConvertible,
    on: Hierarchy,
    /,
    *,
    offset: str,
    method: _DateShiftMethod = "exact",
) -> MeasureDescription:
    """Return a measure equal to the passed measure shifted to another date.

    Args:
        measure: The measure to shift.
        on: The hierarchy to shift on.
            Only hierarchies with their last level of type date (or datetime) are supported.
            If one of the member of the hierarchy is ``N/A`` their shifted value will always be ``None``.
        offset: The period to shift by as specified by `Java's Period.parse() <https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/time/Period.html#parse(java.lang.CharSequence)>`__.
        method: Determine the value to use when there is no member at the shifted date:

            * ``exact``: ``None``.
            * ``previous``: Value at the previous existing date.
            * ``next``: Value at the next existing date.
            * ``interpolate``: Linear interpolation of the values at the previous and next existing dates.

    Example:
        .. doctest::
            :hide:

            >>> session = getfixture("default_session")

        >>> from datetime import date
        >>> df = pd.DataFrame(
        ...     columns=["Date", "Price"],
        ...     data=[
        ...         (date(2020, 8, 1), 5),
        ...         (date(2020, 8, 15), 7),
        ...         (date(2020, 8, 30), 15),
        ...         (date(2020, 8, 31), 15),
        ...         (date(2020, 9, 1), 10),
        ...         (date(2020, 9, 30), 21),
        ...         (date(2020, 10, 1), 9),
        ...         (date(2020, 10, 31), 8),
        ...     ],
        ... )
        >>> table = session.read_pandas(
        ...     df,
        ...     table_name="date_shift example",
        ... )
        >>> cube = session.create_cube(table)
        >>> h, l, m = cube.hierarchies, cube.levels, cube.measures
        >>> cube.create_date_hierarchy(
        ...     "Date parts", column=table["Date"], levels={"Year": "y", "Month": "M"}
        ... )
        >>> h["Date"] = {**h["Date parts"], "Date": table["Date"]}
        >>> m["Exact"] = tt.date_shift(
        ...     m["Price.SUM"], h["Date"], offset="P1M", method="exact"
        ... )
        >>> m["Exact in the past"] = tt.date_shift(
        ...     m["Price.SUM"], h["Date"], offset="-P1M", method="exact"
        ... )
        >>> m["Previous"] = tt.date_shift(
        ...     m["Price.SUM"], h["Date"], offset="P1M", method="previous"
        ... )
        >>> m["Next"] = tt.date_shift(
        ...     m["Price.SUM"], h["Date"], offset="P1M", method="next"
        ... )
        >>> m["Interpolate"] = tt.date_shift(
        ...     m["Price.SUM"], h["Date"], offset="P1M", method="interpolate"
        ... )
        >>> cube.query(
        ...     m["Price.SUM"],
        ...     m["Exact"],
        ...     m["Exact in the past"],
        ...     m["Previous"],
        ...     m["Next"],
        ...     m["Interpolate"],
        ...     levels=[l["Date"]],
        ...     include_totals=True,
        ... )
                               Price.SUM Exact Exact in the past Previous Next Interpolate
        Year  Month Date
        Total                         90
        2020                          90
              8                       42
                    2020-08-01         5    10                         10   10       10.00
                    2020-08-15         7                               10   21       15.31
                    2020-08-30        15    21                         21   21       21.00
                    2020-08-31        15    21                         21   21       21.00
              9                       31
                    2020-09-01        10     9                 5        9    9        9.00
                    2020-09-30        21                      15        9    8        8.03
              10                      17
                    2020-10-01         9                      10        8
                    2020-10-31         8                      21        8

        Explanations for values:

        * :guilabel:`Exact`
            * The value for ``2020-08-31`` is taken from ``2020-09-30`` because there is no 31st of September.
        * :guilabel:`Exact in the past`
            * The value for ``2020-10-31`` is taken from ``2020-09-30`` for the same reason.
        * :guilabel:`Interpolate`
            * ``10.00, 21.00, 21.00, 9.00``: no interpolation is required since there is an exact match.
            * ``15.31``: linear interpolation of ``2020-09-01``'s ``10`` and ``2020-09-30``'s ``21`` at ``2020-08-15``.
            * ``8.03``: linear interpolation of ``2020-10-01``'s ``9`` and ``2020-10-31``'s ``8`` at ``2020-09-30``.
            * ∅: no interpolation possible because there are no records after ``2020-10-31``.

    """
    if not is_temporal_type(list(on.values())[-1].data_type):
        raise ValueError(
            f"The hierarchy {on.name} should have a temporal deepest level.",
        )
    return DateShift(
        _underlying_measure=convert_to_measure_description(measure),
        _level_identifier=list(on.values())[-1]._identifier,
        _shift=offset,
        _method=method,
    )
