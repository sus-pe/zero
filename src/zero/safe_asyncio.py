import asyncio
from collections.abc import Coroutine
from typing import Any

from zero.contextmanagers import assert_raises


def run[T](coroutine: Coroutine[Any, Any, T]) -> T:
    with assert_raises(RuntimeError, "no running event loop"):
        asyncio.get_running_loop()

    return asyncio.run(coroutine)
