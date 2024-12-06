from __future__ import annotations

import json
from abc import ABC
from collections.abc import Collection
from dataclasses import field
from typing import Final, Literal, final
from urllib.parse import urlencode

import httpx
from pydantic import ConfigDict
from pydantic.dataclasses import dataclass

from ._activeviam_client import ActiveViamClient
from ._collections import FrozenMapping, FrozenSequence
from ._pydantic import (
    PYDANTIC_CONFIG as __PYDANTIC_CONFIG,
    create_camel_case_alias_generator,
    get_type_adapter,
)

_PYDANTIC_CONFIG: ConfigDict = {
    **__PYDANTIC_CONFIG,
    "alias_generator": create_camel_case_alias_generator(
        force_aliased_attribute_names={"is_directory"},
    ),
    "arbitrary_types_allowed": False,
    "extra": "ignore",
}


_USER_CONTENT_STORAGE_NAMESPACE = "activeviam/content"


@dataclass(config=_PYDANTIC_CONFIG, frozen=True, kw_only=True)
class _ContentEntry(ABC):
    timestamp: int
    last_editor: str
    owners: FrozenSequence[str]
    readers: FrozenSequence[str]
    can_read: bool
    can_write: bool


@final
@dataclass(config=_PYDANTIC_CONFIG, frozen=True, kw_only=True)
class DirectoryContentEntry(_ContentEntry):
    is_directory: Literal[True] = field(default=True, repr=False)


@final
@dataclass(config=_PYDANTIC_CONFIG, frozen=True, kw_only=True)
class DirectoryContentTree:
    entry: DirectoryContentEntry
    children: FrozenMapping[str, ContentTree] = field(default_factory=dict)


@final
@dataclass(config=_PYDANTIC_CONFIG, frozen=True, kw_only=True)
class FileContentEntry(_ContentEntry):
    content: str
    is_directory: Literal[False] = field(default=False, repr=False)


@final
@dataclass(config=_PYDANTIC_CONFIG, frozen=True, kw_only=True)
class FileContentTree:
    entry: FileContentEntry


ContentTree = DirectoryContentTree | FileContentTree


@final
class ContentClient:
    def __init__(self, *, activeviam_client: ActiveViamClient) -> None:
        self._activeviam_client: Final = activeviam_client

    def _get_path(self, path: str, /) -> str:
        return f"{self._activeviam_client.get_endpoint_path(namespace=_USER_CONTENT_STORAGE_NAMESPACE,route='files')}?{urlencode({'path': path})}"

    def get(self, path: str, /) -> ContentTree | None:
        path = self._get_path(path)
        response = self._activeviam_client.http_client.get(path)
        if response.status_code == httpx.codes.NOT_FOUND:
            return None
        response.raise_for_status()
        body = response.content
        return get_type_adapter(ContentTree).validate_json(body)  # type: ignore[arg-type] # pyright: ignore[reportArgumentType]

    def create(
        self,
        path: str,
        /,
        *,
        content: object,
        owners: Collection[str],
        readers: Collection[str],
    ) -> None:
        path = self._get_path(path)
        self._activeviam_client.http_client.put(
            path,
            json={
                "content": json.dumps(content),
                "owners": list(owners),
                "readers": list(readers),
                "overwrite": True,
                "recursive": True,
            },
        ).raise_for_status()

    def delete(self, path: str, /) -> None:
        path = self._get_path(path)
        self._activeviam_client.http_client.delete(path).raise_for_status()
