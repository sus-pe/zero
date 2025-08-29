import pytest

from zero.contextmanagers import assert_raises


def always_fail(e: type[BaseException], msg: str) -> None:
    raise e(msg)


def test_assert_raises() -> None:
    msg = "Stub Message"
    e = AssertionError
    with assert_raises(e, msg):
        always_fail(e, msg)

    with pytest.raises(AssertionError), assert_raises(e, msg):
        pass
