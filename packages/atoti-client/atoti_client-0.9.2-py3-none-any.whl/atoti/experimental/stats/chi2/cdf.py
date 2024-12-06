from __future__ import annotations

from ...._measure.calculated_measure import CalculatedMeasure, Operator
from ...._measure_convertible import VariableMeasureConvertible
from ...._measure_description import MeasureDescription, convert_to_measure_description
from .._strictly_positive_number import StrictlyPositiveNumber


def cdf(
    point: VariableMeasureConvertible,
    /,
    *,
    degrees_of_freedom: StrictlyPositiveNumber | VariableMeasureConvertible,
) -> MeasureDescription:
    r"""Cumulative distribution function for a chi-square distribution.

    The cdf of the chi-square distribution with k degrees of freedom is

    .. math::

        \operatorname {cdf}(x)=\dfrac {\gamma (\frac {k}{2},\,\frac {x}{2})}{\Gamma (\frac {k}{2})}

    where :math:`\Gamma` is the `gamma function <https://en.wikipedia.org/wiki/Gamma_function>`__
    and :math:`\gamma` the `lower incomplete gamma function <https://en.wikipedia.org/wiki/Incomplete_gamma_function>`__.

    Args:
        point: The point where the function is evaluated.
        degrees_of_freedom: The number of degrees of freedom.
            Must be positive.

    See Also:
        `The Chi-square Wikipedia page <https://en.wikipedia.org/wiki/Chi-square_distribution>`__.

    """
    return CalculatedMeasure(
        Operator(
            "chi2_cumulative_probability",
            [
                convert_to_measure_description(arg)
                for arg in [point, degrees_of_freedom]
            ],
        ),
    )
