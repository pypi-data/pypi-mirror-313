from __future__ import annotations

from ...._measure.calculated_measure import CalculatedMeasure, Operator
from ...._measure_convertible import VariableMeasureConvertible
from ...._measure_description import MeasureDescription, convert_to_measure_description
from .._strictly_positive_number import StrictlyPositiveNumber


def pdf(
    point: VariableMeasureConvertible,
    /,
    *,
    numerator_degrees_of_freedom: StrictlyPositiveNumber | VariableMeasureConvertible,
    denominator_degrees_of_freedom: StrictlyPositiveNumber | VariableMeasureConvertible,
) -> MeasureDescription:
    r"""Probability density function for a F-distribution.

    The pdf for a F-distributions with parameters :math:`d1` et :math:`d2` is

    .. math::

        \operatorname {pdf}(x) = \frac
          {\sqrt {\frac {(d_{1}x)^{d_{1}}\,\,d_{2}^{d_{2}}}{(d_{1}x+d_{2})^{d_{1}+d_{2}}}}}
          {x\,\mathrm {B} \!\left(\frac {d_{1}}{2},\frac {d_{2}}{2}\right)}

    Where :math:`\mathrm {B}` is the beta function.

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
            "F_density",
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
