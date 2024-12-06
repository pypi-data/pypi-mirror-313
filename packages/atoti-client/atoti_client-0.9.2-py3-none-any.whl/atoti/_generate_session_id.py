from random import choices
from string import digits
from time import time


def generate_session_id() -> str:
    random_string = "".join(
        # No cryptographic security required.
        choices(digits, k=6),  # noqa: S311
    )
    return f"{int(time())}_{random_string}"
