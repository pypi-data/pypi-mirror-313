from __future__ import annotations

from ...._measure.calculated_measure import CalculatedMeasure, Operator
from ...._measure_convertible import VariableMeasureConvertible
from ...._measure_description import MeasureDescription, convert_to_measure_description
from .._numeric_measure_convertible import NumericMeasureConvertible
from .._strictly_positive_number import StrictlyPositiveNumber


def ppf(
    point: VariableMeasureConvertible,
    /,
    *,
    mean: NumericMeasureConvertible,
    standard_deviation: StrictlyPositiveNumber | VariableMeasureConvertible,
) -> MeasureDescription:
    r"""Percent point function for a normal distribution.

    Also called inverse cumulative distribution function.

    The ppf is given by the formula

    .. math::

       \operatorname {ppf}(x) = \mu + \sigma \sqrt{2} \operatorname {erf} ^{-1}(2x-1)

    Where :math:`\mu` is the mean of the distribution, :math:`\sigma` is its standard deviation and :math:`\operatorname {erf}^{-1}` the inverse of the error function.

    Args:
        point: The point where the function is evaluated.
        mean: The mean value of the distribution.
        standard_deviation: The standard deviation of the distribution.
            Must be positive.

    See Also:
        `Quantile function of a normal distribution <https://en.wikipedia.org/wiki/Normal_distribution#Quantile_function>`__.

    """
    return CalculatedMeasure(
        Operator(
            "normal_ppf",
            [
                convert_to_measure_description(arg)
                for arg in [point, mean, standard_deviation]
            ],
        ),
    )
