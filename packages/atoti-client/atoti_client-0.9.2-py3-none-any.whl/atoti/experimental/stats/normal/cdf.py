from __future__ import annotations

from ...._measure.calculated_measure import CalculatedMeasure, Operator
from ...._measure_convertible import VariableMeasureConvertible
from ...._measure_description import MeasureDescription, convert_to_measure_description
from .._numeric_measure_convertible import NumericMeasureConvertible
from .._strictly_positive_number import StrictlyPositiveNumber


def cdf(
    point: VariableMeasureConvertible,
    /,
    *,
    mean: NumericMeasureConvertible,
    standard_deviation: StrictlyPositiveNumber | VariableMeasureConvertible,
) -> MeasureDescription:
    r"""Cumulative distribution function for a normal distribution.

    The cdf is given by the formula

    .. math::

       \operatorname {cdf}(x) = \frac {1}{2}\left[1 + \operatorname {erf} \left(\frac {x-\mu }{\sigma {\sqrt {2}}}\right)\right]

    Where :math:`\mu` is the mean of the distribution, :math:`\sigma` is its standard deviation and :math:`\operatorname {erf}` the error function.

    Args:
        point: The point where the function is evaluated.
        mean: The mean value of the distribution.
        standard_deviation: The standard deviation of the distribution.
            Must be positive.

    See Also:
        `cdf of a normal distribution <https://en.wikipedia.org/wiki/Normal_distribution#Cumulative_distribution_function>`__.

    """
    return CalculatedMeasure(
        Operator(
            "normal_cumulative_probability",
            [
                convert_to_measure_description(arg)
                for arg in [point, mean, standard_deviation]
            ],
        ),
    )
