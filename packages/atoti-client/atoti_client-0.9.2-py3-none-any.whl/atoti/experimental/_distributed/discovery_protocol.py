from abc import ABC, abstractmethod
from typing import final

from ..._pydantic import get_type_adapter


def _stringify_property(value: object) -> str:
    if isinstance(value, bool):
        return str(value).lower()
    if isinstance(value, int):
        return str(value)
    if isinstance(value, str):
        return value
    raise TypeError(f"Unsupported property type: `{type(value)}`.")


class DiscoveryProtocol(ABC):
    @property
    @abstractmethod
    def _protocol_name(self) -> str: ...

    @property
    def _properties(self) -> dict[str, object]:
        type_adapter = get_type_adapter(type(self))
        properties = type_adapter.dump_python(self, by_alias=True)
        assert isinstance(properties, dict)
        return properties

    @final
    @property
    def _xml(self) -> str:
        stringified_properties = " ".join(
            f'{key}="{_stringify_property(value)}"'
            for key, value in self._properties.items()
            if value is not None
        )
        return f"<{self._protocol_name} {stringified_properties} />"
