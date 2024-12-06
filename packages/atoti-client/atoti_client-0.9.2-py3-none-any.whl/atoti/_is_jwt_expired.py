import json
from base64 import b64decode
from datetime import timedelta
from time import time


def _parse_jwt_claims(jwt: str, /) -> dict[str, object]:
    claims: dict[str, object] = json.loads(b64decode(jwt.split(".")[1]))
    return claims


_DEFAULT_MARGIN = timedelta(minutes=30)


def is_jwt_expired(jwt: str, /, *, margin: timedelta = _DEFAULT_MARGIN) -> bool:
    claims = _parse_jwt_claims(jwt)

    expiry = claims.get("exp")

    if expiry is None:
        return False

    assert isinstance(expiry, int | str)

    now = time()
    return (now + margin.total_seconds()) > int(expiry)
