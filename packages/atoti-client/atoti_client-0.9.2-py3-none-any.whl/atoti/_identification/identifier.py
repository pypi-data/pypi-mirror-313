from abc import ABC, abstractmethod

from typing_extensions import override


class Identifier(ABC):
    @abstractmethod
    @override
    def __repr__(self) -> str: ...

    @override
    def __str__(self) -> str:
        return repr(self)
