from collections.abc import Generator
from contextlib import contextmanager

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
