from typing import Final, final

from typing_extensions import override

from .._identification import MeasureIdentifier
from .._java_api import JavaApi
from .._measure_description import MeasureDescription
from .utils import convert_measure_args


@final
class GenericMeasure(MeasureDescription):
    """Generic implementation of a MeasureDescription."""

    def __init__(self, plugin_key: str, /, *args: object):
        """Create the measure.

        Args:
            args: The arguments used to create the measure.
                They are directly forwarded to the Java code, except for the ``Measure``
                arguments that are first created on the Java side and replaced by their name.
            plugin_key: The plugin key of the Java implementation.
        """
        self._args: Final = args
        self._plugin_key: Final = plugin_key

    @override
    def _do_distil(
        self,
        identifier: MeasureIdentifier | None = None,
        /,
        *,
        cube_name: str,
        java_api: JavaApi,
    ) -> MeasureIdentifier:
        return java_api.create_measure(
            identifier,
            self._plugin_key,
            *convert_measure_args(
                java_api=java_api,
                cube_name=cube_name,
                args=self._args,
            ),
            cube_name=cube_name,
        )
