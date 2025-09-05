import asyncio
from collections.abc import Coroutine
from types import TracebackType
from typing import Any

from zero.contextmanagers import (
    CONTEXT_MANAGER_EXIT_DO_NOT_SUPPRESS_EXCEPTION,
    assert_raises,
)


def run[T](coroutine: Coroutine[Any, Any, T]) -> T:
    with assert_raises(RuntimeError, "no running event loop"):
        asyncio.get_running_loop()

    return asyncio.run(coroutine)


class AsyncLeakDetector:
    async def __aenter__(self) -> "AsyncLeakDetector":
        self.loop = asyncio.get_running_loop()
        self.before = set(asyncio.all_tasks(self.loop))
        return self

    async def __aexit__(
        self,
        _exc_type: type[BaseException] | None,
        _exc_val: BaseException | None,
        _exc_tb: TracebackType | None,
    ) -> bool | None:
        after = set(asyncio.all_tasks(self.loop)) - self.before
        leaked = [t for t in after if not t.done()]
        assert not leaked, f"Leaked: {leaked}"
        return CONTEXT_MANAGER_EXIT_DO_NOT_SUPPRESS_EXCEPTION
