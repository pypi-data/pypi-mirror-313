from dataclasses import KW_ONLY
from typing import final

from pydantic.dataclasses import dataclass
from typing_extensions import override

from .._graphql_client import CubeIdentifierInput
from ._identifier_pydantic_config import IDENTIFIER_PYDANTIC_CONFIG
from .cube_name import CubeName
from .identifier import Identifier


@final
@dataclass(config=IDENTIFIER_PYDANTIC_CONFIG, frozen=True)
class CubeIdentifier(Identifier):
    cube_name: CubeName
    _: KW_ONLY

    @property
    def _graphql_input(self) -> CubeIdentifierInput:
        return CubeIdentifierInput(cube_name=self.cube_name)

    @override
    def __repr__(self) -> str:
        return f"""c["{self.cube_name}"]"""
