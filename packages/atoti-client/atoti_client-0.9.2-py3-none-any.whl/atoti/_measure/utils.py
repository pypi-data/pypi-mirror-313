from collections.abc import Collection, Mapping
from typing import cast

from .._constant import Constant
from .._identification import HasIdentifier, MeasureIdentifier
from .._java_api import JavaApi
from .._measure_convertible import MeasureConvertible
from .._measure_description import MeasureDescription, convert_to_measure_description
from .._operation import Condition, Operation
from .._py4j_utils import to_java_object, to_java_object_array


def get_measure_name(
    *,
    java_api: JavaApi,
    measure: MeasureDescription,
    cube_name: str,
) -> str:
    """Get the name of the measure from either a measure or its name."""
    return measure._distil(java_api=java_api, cube_name=cube_name).measure_name


def convert_measure_args(
    *,
    java_api: JavaApi,
    cube_name: str,
    args: Collection[object],
) -> list[object]:
    """Convert arguments used for creating a measure in Java.

    The ``Measure`` arguments are replaced by their name, and other arguments are
    translated into Java-equivalent objects when necessary.
    """
    return [
        _convert_measure_arg(java_api=java_api, cube_name=cube_name, arg=a)
        for a in args
    ]


def _convert_measure_arg(  # noqa: PLR0911
    *,
    java_api: JavaApi,
    cube_name: str,
    arg: object,
) -> object:
    # Replace measures with their name.
    if isinstance(arg, MeasureDescription):
        return get_measure_name(java_api=java_api, measure=arg, cube_name=cube_name)

    if isinstance(arg, HasIdentifier) and isinstance(
        arg._identifier,
        MeasureIdentifier,
    ):
        return arg._identifier.measure_name

    if isinstance(arg, Condition | Operation):
        return _convert_measure_arg(
            java_api=java_api,
            cube_name=cube_name,
            arg=convert_to_measure_description(cast(MeasureConvertible, arg)),
        )

    if isinstance(arg, Constant):
        return _convert_measure_arg(
            java_api=java_api,
            cube_name=cube_name,
            arg=convert_to_measure_description(arg.value),
        )

    # Recursively convert nested args.
    if isinstance(arg, tuple):
        return to_java_object_array(
            convert_measure_args(java_api=java_api, cube_name=cube_name, args=arg),
            gateway=java_api.gateway,
        )
    if isinstance(arg, list):
        return convert_measure_args(java_api=java_api, cube_name=cube_name, args=arg)
    if isinstance(arg, Mapping):
        return {
            _convert_measure_arg(
                java_api=java_api,
                cube_name=cube_name,
                arg=key,
            ): _convert_measure_arg(java_api=java_api, cube_name=cube_name, arg=value)
            for key, value in arg.items()
        }

    # Nothing smarter to do. Transform the argument to a java array.
    return to_java_object(arg, gateway=java_api.gateway)
