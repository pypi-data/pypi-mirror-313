from collections.abc import Mapping
from typing import Final, final

import httpx
import pandas as pd
import pyarrow as pa

from .._activeviam_client import ActiveViamClient
from .._pandas import pandas_from_arrow


# Adapted from https://github.com/encode/httpx/discussions/2296#discussioncomment-6781355.
@final
class _FileLikeAdapter:
    def __init__(self, response: httpx.Response, /):
        self._response: Final = response
        self._iterator: Final = response.iter_raw()
        self._buffer = bytearray()
        self._buffer_offset = 0

    @property
    def closed(self) -> bool:
        return self._response.is_closed

    def read(self, size: int = -1) -> bytearray | bytes:
        while len(self._buffer) - self._buffer_offset < size:
            try:
                chunk = next(self._iterator)
                self._buffer += chunk
            except StopIteration:  # noqa: PERF203
                break

        if len(self._buffer) - self._buffer_offset >= size:
            data = self._buffer[self._buffer_offset : self._buffer_offset + size]
            self._buffer_offset += size
            return data

        data = self._buffer[self._buffer_offset :]
        self._buffer.clear()
        self._buffer_offset = 0
        return data


def execute_arrow_query(
    *,
    activeviam_client: ActiveViamClient,
    body: Mapping[str, object],
    path: str,
) -> pd.DataFrame:
    with activeviam_client.http_client.stream(
        "POST",
        path,
        json=body,
        # The timeout should be part of `body` and will be managed by the server.
        timeout=None,
    ) as response:
        source = _FileLikeAdapter(response)
        record_batch_stream = pa.ipc.open_stream(source)
        schema = record_batch_stream.schema
        for name in schema.names:
            schema.field(name).with_nullable(True)  # noqa: FBT003
        table = pa.Table.from_batches(record_batch_stream, schema=schema)

    return pandas_from_arrow(table)
