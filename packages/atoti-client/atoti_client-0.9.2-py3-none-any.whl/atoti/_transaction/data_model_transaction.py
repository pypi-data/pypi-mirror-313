from __future__ import annotations

from collections.abc import Callable
from contextlib import AbstractContextManager
from contextvars import ContextVar

from ._transact import transact
from ._transaction_context import TransactionContext

_CONTEXT_VAR: ContextVar[TransactionContext] = ContextVar(
    "atoti_data_model_transaction",
)


def is_transacting_data_model() -> bool:
    return _CONTEXT_VAR.get(None) is not None


def transact_data_model(
    *,
    allow_nested: bool,
    commit: Callable[..., None],
    session_id: str,
) -> AbstractContextManager[None]:
    def start() -> str:
        # In the future, Atoti Server will be aware of the data model transaction and provide its ID to the client.
        return "unused"

    def rollback(
        transaction_id: str,
    ) -> None:
        # Rollback of data model transactions is not supported yet.
        ...

    return transact(
        allow_nested=allow_nested,
        commit=lambda _: commit(),
        context_var=_CONTEXT_VAR,
        rollback=rollback,
        session_id=session_id,
        start=start,
    )
