from __future__ import annotations

from ...._measure.calculated_measure import CalculatedMeasure, Operator
from ...._measure_convertible import VariableMeasureConvertible
from ...._measure_description import MeasureDescription, convert_to_measure_description
from .._strictly_positive_number import StrictlyPositiveNumber


def ppf(
    point: VariableMeasureConvertible,
    /,
    *,
    numerator_degrees_of_freedom: StrictlyPositiveNumber | VariableMeasureConvertible,
    denominator_degrees_of_freedom: StrictlyPositiveNumber | VariableMeasureConvertible,
) -> MeasureDescription:
    """Percent point function for a F-distribution.

    Also called inverse cumulative distribution function.

    Args:
        point: The point where the function is evaluated.
        numerator_degrees_of_freedom: Numerator degrees of freedom.
            Must be positive.
        denominator_degrees_of_freedom: Denominator degrees of freedom.
            Must be positive.

    See Also:
        `The F-distribution Wikipedia page <https://en.wikipedia.org/wiki/F-distribution>`__.

    """
    return CalculatedMeasure(
        Operator(
            "F_ppf",
            [
                convert_to_measure_description(arg)
                for arg in [
                    point,
                    numerator_degrees_of_freedom,
                    denominator_degrees_of_freedom,
                ]
            ],
        ),
    )
