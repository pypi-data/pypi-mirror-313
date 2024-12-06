from __future__ import annotations

from .._measure.generic_measure import GenericMeasure
from .._measure_convertible import MeasureConvertible
from .._measure_description import MeasureDescription, convert_to_measure_description


def concat(*measures: MeasureConvertible, separator: str = "") -> MeasureDescription:
    """Concatenate measures together into a string.

    Args:
        measures: The string measures to concatenate together.
        separator: The separator to place between each measure value.
    """
    underlying_measures = [
        convert_to_measure_description(measure) for measure in measures
    ]
    return GenericMeasure("STRING_CONCAT", separator, underlying_measures)
