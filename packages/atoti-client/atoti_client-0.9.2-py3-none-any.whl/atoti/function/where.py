from __future__ import annotations

from collections.abc import Mapping
from typing import cast, overload

from .._column_convertible import (
    ColumnCondition,
    ColumnConvertible,
    is_column_condition,
    is_variable_column_convertible,
)
from .._identification import ColumnIdentifier, HasIdentifier
from .._measure.filtered_measure import WhereMeasure
from .._measure_convertible import (
    MeasureCondition,
    MeasureConvertible,
    VariableMeasureConvertible,
    is_variable_measure_convertible,
)
from .._measure_description import MeasureDescription, convert_to_measure_description
from .._operation import Condition, Operation, convert_to_operand, decombine_condition
from .._where_operation import WhereOperation


@overload
def where(  # pylint: disable=too-many-positional-parameters
    condition: ColumnCondition,
    true_value: ColumnConvertible,
    # Not keyword-only to be symmetrical with `true_value` and because there probably will not be more optional parameters.
    false_value: ColumnConvertible | None = ...,
    /,
) -> Operation[ColumnIdentifier]: ...


@overload
def where(  # pylint: disable=too-many-positional-parameters
    condition: VariableMeasureConvertible,
    true_value: MeasureConvertible,
    # Not keyword-only to be symmetrical with `true_value` and because there probably will not be more optional parameters.
    false_value: MeasureConvertible | None = ...,
    /,
) -> MeasureDescription: ...


@overload
def where(
    condition_to_value: Mapping[
        VariableMeasureConvertible,
        MeasureConvertible,
    ],
    /,
    *,
    default: MeasureConvertible | None = ...,
) -> MeasureDescription: ...


def where(  # noqa: C901 # pylint: disable=too-many-positional-parameters
    condition_or_condition_to_value: ColumnCondition
    | VariableMeasureConvertible
    | Mapping[VariableMeasureConvertible, MeasureConvertible],
    true_value: ColumnConvertible | MeasureConvertible | None = None,
    false_value: ColumnConvertible | MeasureConvertible | None = None,
    /,
    *,
    default: MeasureConvertible | None = None,
) -> MeasureDescription | Operation[ColumnIdentifier]:
    """Return a conditional measure.

    This function is like an *if-then-else* statement:

    * Where the condition is ``True``, the new measure will be equal to *true_value*.
    * Where the condition is ``False``, the new measure will be equal to *false_value*.

    If *false_value* is not ``None``, *true_value* and *false_value* must either be both numerical, both boolean or both objects.

    If one of the values compared in the condition is ``None``, the condition will be considered ``False``.

    Different types of conditions are supported:

    * Measures compared to anything measure-like::

        m["Test"] == 20

    * Levels compared to levels, (if the level is not expressed, it is considered ``None``)::

        l["source"] == l["destination"]

    * Levels compared to constants of the same type::

        l["city"] == "Paris"
        l["date"] > datetime.date(2020, 1, 1)
        l["age"] <= 18

    * A conjunction or disjunction of conditions using the ``&`` operator or ``|`` operator::

        (m["Test"] == 20) & (l["city"] == "Paris")
        (l["Country"] == "USA") | (l["Currency"] == "USD")


    Example:
        .. doctest::
            :hide:

            >>> session = getfixture("default_session")

        >>> df = pd.DataFrame(
        ...     columns=["Id", "City", "Value"],
        ...     data=[
        ...         (0, "Paris", 1.0),
        ...         (1, "Paris", 2.0),
        ...         (2, "London", 3.0),
        ...         (3, "London", 4.0),
        ...         (4, "Paris", 5.0),
        ...     ],
        ... )
        >>> table = session.read_pandas(df, keys={"Id"}, table_name="filter example")
        >>> cube = session.create_cube(table)
        >>> l, m = cube.levels, cube.measures
        >>> m["Paris value"] = tt.where(l["City"] == "Paris", m["Value.SUM"], 0)
        >>> cube.query(m["Paris value"], levels=[l["City"]])
               Paris value
        City
        London         .00
        Paris         8.00

        When a mapping of condition to value is passed, the resulting value is the one of the first condition evaluating to ``True``:

        >>> m["Value.RECAP"] = tt.where(
        ...     {
        ...         m["Value.SUM"] < 3: "less than 3",
        ...         m["Value.SUM"] <= 3: "less than or equal to 3",
        ...         m["Value.SUM"]
        ...         == 3: "equal to 3",  # never used because of the broader condition before
        ...     },
        ...     default="more than 3",
        ... )
        >>> cube.query(m["Value.SUM"], m["Value.RECAP"], levels=[l["Id"]])
           Value.SUM              Value.RECAP
        Id
        0       1.00              less than 3
        1       2.00              less than 3
        2       3.00  less than or equal to 3
        3       4.00              more than 3
        4       5.00              more than 3

    See Also:
        :func:`atoti.switch`.
    """
    if isinstance(condition_or_condition_to_value, Condition) and is_column_condition(
        condition_or_condition_to_value,
    ):
        column_condition = condition_or_condition_to_value

        if true_value is None or is_variable_measure_convertible(true_value):
            raise ValueError(
                f"Expected a non-None and column convertible `true_value` but got `{true_value}`.",
            )

        if is_variable_measure_convertible(false_value):
            raise ValueError(
                f"Expected a column convertible `false_value` but got `{false_value}`.",
            )

        return WhereOperation(
            condition=column_condition,
            true_value=convert_to_operand(true_value),
            false_value=convert_to_operand(false_value),
        )

    if isinstance(condition_or_condition_to_value, Mapping):
        condition_to_value = condition_or_condition_to_value

        measures_and_conditions: list[
            tuple[MeasureDescription, tuple[MeasureDescription, ...]]
        ] = []

        for case_condition, value in condition_to_value.items():
            conditions: list[VariableMeasureConvertible] = []

            if isinstance(case_condition, Condition):
                decombined_conditions = decombine_condition(case_condition)  # type: ignore[var-annotated]

                if len(decombined_conditions) == 1:
                    (
                        comparison_conditions,
                        isin_conditions,
                        hierarchy_isin_conditions,
                    ) = decombined_conditions[0]

                    conditions.extend(
                        convert_to_measure_description(
                            # `case_condition` is a `MeasureCondition` so its sub conditions are too.
                            # Casting here to avoid having to repeat all the measure related constraints when calling `decombine_condition()`.
                            cast(MeasureCondition, sub_condition),
                        )
                        for sub_condition in [
                            *comparison_conditions,
                            *isin_conditions,
                            *hierarchy_isin_conditions,
                        ]
                    )
                else:
                    conditions.append(convert_to_measure_description(case_condition))
            else:
                assert isinstance(
                    case_condition,
                    HasIdentifier | MeasureDescription,
                ), f"Unexpected condition type: `{type(case_condition).__name__}`."
                conditions.append(case_condition)

            measures_and_conditions.append(
                (
                    convert_to_measure_description(value),
                    tuple(
                        convert_to_measure_description(condition)
                        for condition in conditions
                    ),
                ),
            )

        return WhereMeasure(
            _measures_and_conditions=measures_and_conditions,
            _default_measure=convert_to_measure_description(default)
            if default is not None
            else None,
        )

    measure_condition = condition_or_condition_to_value

    if not is_variable_measure_convertible(measure_condition):
        raise ValueError(
            f"Expected a variable measure convertible `condition` but got `{measure_condition}`.",
        )

    if true_value is None or is_variable_column_convertible(true_value):
        raise ValueError(
            f"Expected a non-None measure convertible `true_value` but got `{true_value}`.",
        )

    if is_variable_column_convertible(false_value):
        raise ValueError(
            f"Expected a measure convertible `false_value` but got `{false_value}`.",
        )

    return where({measure_condition: true_value}, default=false_value)
