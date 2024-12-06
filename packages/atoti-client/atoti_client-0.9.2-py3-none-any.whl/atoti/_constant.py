from __future__ import annotations

import json
import math
import re
from collections.abc import Sequence
from dataclasses import field
from datetime import date, datetime, time, timedelta, timezone
from typing import Annotated, TypeAlias, cast, final
from zoneinfo import ZoneInfo

from pydantic import BeforeValidator, PlainSerializer, ValidationInfo
from pydantic.dataclasses import dataclass
from typing_extensions import Self, override

from ._data_type import (
    DataType,
    data_type_from_graphql as _data_type_from_graphql,
    data_type_to_graphql as _data_type_to_graphql,
)
from ._java import JAVA_INT_RANGE
from ._pydantic import create_camel_case_alias_generator, get_type_adapter


def _parse_data_type(data_type: str, /) -> str:
    # Nested import required to avoid circular import caused by custom `Constant` scalar.
    from ._graphql_client import (  # pylint: disable=nested-import
        DataType as GraphQlDataType,
    )

    return (
        _data_type_from_graphql(GraphQlDataType[data_type])
        if data_type in GraphQlDataType.__members__
        else data_type
    )


_NaN = "NaN"
_NEGATIVE_INFINITY = "-Infinity"
_POSITIVE_INFINITY = "Infinity"


def _validate_float(value: object, /) -> float:
    if isinstance(value, float):
        return value

    if isinstance(value, int):
        return float(value)

    if isinstance(value, str):
        if value == _NaN:
            return math.nan
        if value == _NEGATIVE_INFINITY:
            return -math.inf
        if value == _POSITIVE_INFINITY:
            return math.inf

    raise ValueError(f"Unsupported value `{value}`.")


_DATE_TIME_PATTERN = re.compile(
    r"^(?P<date_time>[^[]+)(\[(?P<timezone_name>[^-+]+)((?P<timezone_offset>.+))?\])?$",
)


def _parse_datetime(value: str, /) -> datetime:
    match = _DATE_TIME_PATTERN.match(value)

    if not match:
        raise ValueError(
            f"`{value}` does not match expected format `{_DATE_TIME_PATTERN}`.",
        )

    datetime_value = get_type_adapter(datetime).validate_python(
        match.group("date_time"),
    )
    timezone_name = match.group("timezone_name")
    formatted_timezone_offset = match.group("timezone_offset")

    if formatted_timezone_offset:
        assert timezone_name
        timezone_offset = get_type_adapter(timedelta).validate_python(
            formatted_timezone_offset,
        )
        return datetime_value.replace(
            tzinfo=timezone(timezone_offset, timezone_name),
        )
    if timezone_name:
        return datetime_value.replace(tzinfo=ZoneInfo(timezone_name))
    return datetime_value


ConstantValue: TypeAlias = (
    bool
    | int
    | float
    | date
    | datetime
    | time
    | Sequence[bool]
    | Sequence[int]
    | Sequence[float]
    | Sequence[str]
    | str
)


def _parse_value(  # noqa: C901, PLR0911, PLR0912
    value: ConstantValue,
    validation_info: ValidationInfo,
    /,
) -> ConstantValue:
    data_type = cast(DataType, validation_info.data["data_type"])

    match data_type:
        case "boolean":
            assert isinstance(value, bool)
            return value
        case "boolean[]":
            assert isinstance(value, Sequence)
            assert all(isinstance(element, bool) for element in value)
            return tuple(cast(Sequence[bool], value))
        case "double" | "float":
            return _validate_float(value)
        case "double[]" | "float[]":
            assert isinstance(value, Sequence)
            return tuple(_validate_float(element) for element in value)
        case "int":
            assert isinstance(value, int)
            assert value in JAVA_INT_RANGE
            return value
        case "int[]":
            assert isinstance(value, Sequence)
            assert all(
                isinstance(element, int) and (element in JAVA_INT_RANGE)
                for element in value
            )
            return tuple(cast(Sequence[int], value))
        case "LocalDate":
            assert isinstance(value, date | str)
            match value:
                case date():
                    return value
                case str():
                    return get_type_adapter(date).validate_python(value)
        case "LocalDateTime" | "ZonedDateTime":
            assert isinstance(value, datetime | str)
            match value:
                case datetime():
                    return value
                case str():
                    return _parse_datetime(value)
        case "LocalTime":
            assert isinstance(value, str | time)
            match value:
                case str():
                    return get_type_adapter(time).validate_python(value)
                case time():
                    return value
        case "long":
            assert isinstance(value, int)
            return value
        case "long[]":
            assert isinstance(value, Sequence)
            assert all(isinstance(element, int) for element in value)
            return tuple(cast(Sequence[int], value))
        # Remove this case.
        # See https://github.com/activeviam/activepivot/blob/2ae2c77b47ca45d86e89ba12d76f00a301b310fe/atoti/patachou/server/server-base/src/main/java/io/atoti/server/base/private_/pivot/graphql/DataType.java#L12-L13.
        case "Object" | "Object[]":
            raise ValueError(f"Unsupported data type `{data_type}`.")
        case "String":
            assert isinstance(value, str)
            return value
        case "String[]":
            assert isinstance(value, Sequence)
            assert all(isinstance(element, str) for element in value)
            return tuple(cast(Sequence[str], value))


def _infer_data_type(value: ConstantValue, /) -> DataType:  # noqa: C901, PLR0911, PLR0912
    match value:
        case bool():
            return "boolean"
        case int():
            return "int" if value in JAVA_INT_RANGE else "long"
        case float():
            return "double"
        case str():
            return "String"
        case datetime():
            return "LocalDateTime" if value.tzinfo is None else "ZonedDateTime"
        case date():
            return "LocalDate"
        case time():
            return "LocalTime"
        case Sequence():
            if not value:
                raise ValueError(
                    "Empty arrays are not supported because their data type cannot be inferred.",
                )
            match value[0]:
                case bool():
                    return "boolean[]"
                case int() | float():
                    data_types = {_infer_data_type(element) for element in value}
                    if data_types == {"int"}:
                        return "int[]"
                    if data_types == {"int", "long"}:
                        return "long[]"
                    return "double[]"
                case str():
                    return "String[]"


def _serialize_data_type(data_type: DataType, /) -> str:
    return _data_type_to_graphql(data_type).value


def _serialize_float(value: float, /) -> float | str:
    if math.isnan(value):
        return _NaN
    if value == -math.inf:
        return _NEGATIVE_INFINITY
    if value == math.inf:
        return _POSITIVE_INFINITY
    return value


def _serialize_non_zoned_datetime(value: datetime, /) -> str:
    assert value.tzinfo is None
    return (
        value.strftime(r"%Y-%m-%dT%H:%M")
        if value.second == 0 and value.microsecond == 0
        else value.isoformat()
    )


_TRAILING_ZERO_SECONDS = ":00"


def _serialize_datetime(value: datetime, /) -> str:
    if value.tzinfo is None:
        return _serialize_non_zoned_datetime(value)

    if value.tzinfo == ZoneInfo("UTC") or value.tzinfo == timezone.utc:
        return f"{_serialize_non_zoned_datetime(value.replace(tzinfo=None))}Z[UTC]"

    formatted_datetime_with_offset = value.isoformat()
    formatted_date, formatted_time_with_offset = formatted_datetime_with_offset.split(
        "T",
    )
    offset_sign = "+" if "+" in formatted_time_with_offset else "-"

    formatted_datetime_without_offset, formatted_offset = (
        formatted_time_with_offset.rsplit(
            offset_sign,
            maxsplit=1,
        )
    )
    if formatted_datetime_without_offset.endswith(_TRAILING_ZERO_SECONDS):
        formatted_datetime_without_offset = formatted_datetime_without_offset[
            : -len(_TRAILING_ZERO_SECONDS)
        ]
        formatted_datetime_with_offset = f"{formatted_date}T{formatted_datetime_without_offset}{offset_sign}{formatted_offset}"

    formatted_timezone = str(value.tzinfo)

    if isinstance(value.tzinfo, timezone) and formatted_timezone in {
        "GMT",
        "UT",
        "UTC",
    }:
        formatted_timezone = f"{formatted_timezone}{offset_sign}{formatted_offset}"

    return f"{formatted_datetime_with_offset}[{formatted_timezone}]"


def _serialize_value(value: ConstantValue, /) -> object:
    match value:
        case float():
            return _serialize_float(value)
        case Sequence() if not isinstance(value, str):
            return tuple(
                _serialize_float(element) if isinstance(element, float) else element
                for element in value
            )
        case datetime():
            return _serialize_datetime(value)
        case date():
            return value.isoformat()
        case time():
            return (
                value.strftime(r"%H:%M")
                if value.second == 0 and value.microsecond == 0
                else value.isoformat()
            )
        case _:
            return value


_LegacyConstantValueJson = bool | float | int | str


@final
@dataclass(
    config={
        "alias_generator": create_camel_case_alias_generator(),
        "extra": "forbid",
    },
    frozen=True,
    kw_only=True,
    order=True,
)
class Constant:
    data_type: Annotated[
        DataType,
        BeforeValidator(_parse_data_type),
        PlainSerializer(_serialize_data_type),
    ] = field(compare=False, repr=False)
    value: Annotated[
        ConstantValue,
        BeforeValidator(_parse_value),
        PlainSerializer(_serialize_value),
    ]

    @classmethod
    def of(cls, value: ConstantValue, /) -> Self:
        """Use this method to infer the data type from *value*."""
        data_type = _infer_data_type(value)
        return cls(data_type=data_type, value=value)

    @property
    def _legacy_value_json(self) -> _LegacyConstantValueJson:
        result_json = get_type_adapter(type(self)).dump_json(self)
        result = json.loads(result_json)
        assert isinstance(result, dict)
        value = result.get("value")

        if isinstance(value, bool | float | int | str):
            return value

        raise NotImplementedError(
            f"Cannot convert constant `{self.value}` of type `{self.data_type}` to JSON.",
        )

    @override
    def __repr__(self) -> str:
        value = list(self.value) if isinstance(self.value, tuple) else self.value
        return f"{self.__class__.__name__}.{self.of.__name__}({value!r})"

    @override
    def __str__(self) -> str:
        return str(self.value)
