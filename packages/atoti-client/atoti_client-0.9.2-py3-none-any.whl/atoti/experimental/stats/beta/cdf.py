from __future__ import annotations

from ...._measure.calculated_measure import CalculatedMeasure, Operator
from ...._measure_convertible import VariableMeasureConvertible
from ...._measure_description import MeasureDescription, convert_to_measure_description
from .._numeric_measure_convertible import NumericMeasureConvertible


def cdf(
    point: VariableMeasureConvertible,
    /,
    *,
    alpha: NumericMeasureConvertible,
    beta: NumericMeasureConvertible,
) -> MeasureDescription:
    r"""Cumulative distribution function for a beta distribution.

    The cdf of the beta distribution with shape parameters :math:`\alpha` and :math:`\beta` is

    .. math::

        \operatorname {cdf}(x) = I_x(\alpha,\beta)


    Where :math:`I` is the `regularized incomplete beta function <https://en.wikipedia.org/wiki/Beta_function#Incomplete_beta_function>`__.

    Args:
        point: The point where the function is evaluated.
        alpha: The alpha parameter of the distribution.
        beta: The beta parameter of the distribution.

    See Also:
        `The beta distribution Wikipedia page <https://en.wikipedia.org/wiki/Beta_distribution>`__.

    """
    return CalculatedMeasure(
        Operator(
            "beta_cumulative_probability",
            [convert_to_measure_description(arg) for arg in [point, alpha, beta]],
        ),
    )
