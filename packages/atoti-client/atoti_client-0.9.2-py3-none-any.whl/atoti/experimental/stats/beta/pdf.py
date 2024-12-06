from __future__ import annotations

from ...._measure.calculated_measure import CalculatedMeasure, Operator
from ...._measure_convertible import VariableMeasureConvertible
from ...._measure_description import MeasureDescription, convert_to_measure_description
from .._numeric_measure_convertible import NumericMeasureConvertible


def pdf(
    point: VariableMeasureConvertible,
    /,
    *,
    alpha: NumericMeasureConvertible,
    beta: NumericMeasureConvertible,
) -> MeasureDescription:
    r"""Probability density function for a beta distribution.

    The pdf of the beta distribution with shape parameters :math:`\alpha` and :math:`\beta` is given by the formula

    .. math::

        \operatorname {pdf}(x) = \frac {x^{\alpha -1}(1-x)^{\beta -1}}{ \mathrm {B}(\alpha ,\beta )}

    With :math:`\mathrm {B}` the beta function:

    .. math::

        \mathrm {B} (\alpha ,\beta )=\int _{0}^{1}t^{\alpha -1}(1-t)^{\beta-1}dt = \frac {\Gamma (\alpha )\Gamma (\beta )}{\Gamma (\alpha +\beta )}


    Where :math:`\Gamma` is the `Gamma function <https://en.wikipedia.org/wiki/Gamma_function>`__.

    Args:
        point: The point where the function is evaluated.
        alpha: The alpha parameter of the distribution.
        beta: The beta parameter of the distribution.

    See Also:
        `The beta distribution Wikipedia page <https://en.wikipedia.org/wiki/Beta_distribution>`__.

    """
    return CalculatedMeasure(
        Operator(
            "beta_density",
            [convert_to_measure_description(arg) for arg in [point, alpha, beta]],
        ),
    )
