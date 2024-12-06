from __future__ import annotations

from collections.abc import Callable
from contextlib import AbstractContextManager
from contextvars import ContextVar

from ._transact import transact
from ._transaction_context import TransactionContext

_CONTEXT_VAR: ContextVar[TransactionContext] = ContextVar(
    "atoti_data_transaction",
)


def is_transacting_data() -> bool:
    return _CONTEXT_VAR.get(None) is not None


def transact_data(
    *,
    allow_nested: bool,
    commit: Callable[[str], None],
    rollback: Callable[[str], None],
    session_id: str,
    start: Callable[[], str],
) -> AbstractContextManager[None]:
    return transact(
        allow_nested=allow_nested,
        commit=commit,
        context_var=_CONTEXT_VAR,
        rollback=rollback,
        session_id=session_id,
        start=start,
    )
