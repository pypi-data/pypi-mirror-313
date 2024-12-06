from .._activeviam_client import ActiveViamClient
from .._context import Context
from .._query_explanation import QueryExplanation
from .._typing import Duration
from ._enrich_mdx_query_context import enrich_mdx_query_context


def explain_mdx_query(
    *,
    activeviam_client: ActiveViamClient,
    context: Context,
    mdx: str,
    pivot_namespace: str,
    timeout: Duration,
) -> QueryExplanation:
    path = activeviam_client.get_endpoint_path(
        namespace=pivot_namespace,
        route="cube/query/mdx/queryplan",
    )
    context = enrich_mdx_query_context(context, timeout=timeout)

    response = activeviam_client.http_client.post(
        path,
        json={"context": {**context}, "mdx": mdx},
        # The timeout is part of `context` and is managed by the server.
        timeout=None,
    ).raise_for_status()
    body = response.content
    return activeviam_client.get_json_response_body_type_adapter(
        QueryExplanation,  # type: ignore[type-abstract]
    ).validate_json(body)
