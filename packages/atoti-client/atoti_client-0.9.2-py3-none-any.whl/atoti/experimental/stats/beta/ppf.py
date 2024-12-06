from __future__ import annotations

from ...._measure.calculated_measure import CalculatedMeasure, Operator
from ...._measure_convertible import VariableMeasureConvertible
from ...._measure_description import MeasureDescription, convert_to_measure_description
from .._numeric_measure_convertible import NumericMeasureConvertible


def ppf(
    point: VariableMeasureConvertible,
    /,
    *,
    alpha: NumericMeasureConvertible,
    beta: NumericMeasureConvertible,
) -> MeasureDescription:
    """Percent point function for a beta distribution.

    Also called inverse cumulative distribution function.

    Args:
        point: The point where the density function is evaluated.
        alpha: The alpha parameter of the distribution.
        beta: The beta parameter of the distribution.

    See Also:
        `The beta distribution Wikipedia page <https://en.wikipedia.org/wiki/Beta_distribution>`__.

    """
    return CalculatedMeasure(
        Operator(
            "beta_ppf",
            [convert_to_measure_description(arg) for arg in [point, alpha, beta]],
        ),
    )
