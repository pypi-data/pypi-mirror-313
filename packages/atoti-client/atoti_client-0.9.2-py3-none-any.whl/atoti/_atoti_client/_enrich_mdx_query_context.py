from math import ceil

from .._context import Context
from .._typing import Duration


def enrich_mdx_query_context(context: Context, /, *, timeout: Duration) -> Context:
    return {"queriesTimeLimit": ceil(timeout.total_seconds()), **context}
