import httpx


def ping(
    *,
    http_client: httpx.Client,
    path: str,
) -> None:
    response = http_client.get(path).raise_for_status()
    body = response.text
    expected_body = "pong"
    if body != expected_body:
        raise RuntimeError(
            f"Expected `ping()`'s response body to be `{expected_body}` but got `{body}`.",
        )
