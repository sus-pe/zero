import warnings
from collections.abc import Generator
from contextlib import contextmanager
from types import TracebackType

import pygame

type ContextManager[T] = Generator[T, None, None]

CONTEXT_MANAGER_EXIT_DO_NOT_SUPPRESS_EXCEPTION = False


@contextmanager
def assert_raises(
    expected_type: type[BaseException], message: str
) -> ContextManager[None]:
    error_msg = f"Did not raise {expected_type}: {message}"
    try:
        yield
    # ruff: noqa: BLE001
    except BaseException as e:
        caught = e
    else:
        raise AssertionError(error_msg)

    assert type(caught) is expected_type
    assert message in caught.args


@contextmanager
def suppress_no_fast_renderer_warning(
    expected_warning: str = "no fast renderer available",
) -> ContextManager[None]:
    with warnings.catch_warnings():
        warnings.filterwarnings(action="ignore", message=expected_warning)
        yield


class PygameContext:
    def __enter__(self) -> "PygameContext":
        assert not self.is_init()
        pygame.init()
        return self

    def __exit__(
        self,
        _exc_type: type[BaseException] | None,
        _exc_val: BaseException | None,
        _exc_tb: TracebackType | None,
    ) -> bool | None:
        self.assert_init()
        pygame.quit()
        return CONTEXT_MANAGER_EXIT_DO_NOT_SUPPRESS_EXCEPTION

    def is_init(self) -> bool:
        return pygame.get_init()

    def assert_init(self) -> None:
        assert self.is_init()
