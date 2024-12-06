from __future__ import annotations

from collections.abc import Callable, Generator
from contextlib import contextmanager
from contextvars import ContextVar, Token

from ._transaction_context import TransactionContext


@contextmanager
def transact(
    *,
    allow_nested: bool,
    commit: Callable[[str], None],
    context_var: ContextVar[TransactionContext],
    rollback: Callable[[str], None],
    session_id: str,
    start: Callable[[], str],
) -> Generator[None, None, None]:
    token: Token[TransactionContext] | None = None

    previous_context = context_var.get(None)

    if previous_context is not None:
        if previous_context.session_id != session_id:
            raise RuntimeError(
                "Cannot start this transaction inside a transaction started from another session.",
            )

        if not allow_nested:
            raise RuntimeError(
                "Cannot start this transaction inside another transaction since nesting is not allowed.",
            )
    else:
        transaction_id = start()
        context = TransactionContext(
            session_id=session_id,
            transaction_id=transaction_id,
        )
        token = context_var.set(context)

    try:
        yield
    except:
        if token is None:
            # This is a nested transaction, let the outer one handle this.
            ...
        else:
            transaction_id = context_var.get().transaction_id
            context_var.reset(token)
            rollback(transaction_id)

        raise
    else:
        if token is None:
            # This is a nested transaction, let the outer one handle this.
            ...
        else:
            transaction_id = context_var.get().transaction_id
            context_var.reset(token)
            commit(transaction_id)
