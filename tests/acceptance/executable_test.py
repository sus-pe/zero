import sys
from pathlib import Path
from subprocess import run

from pytest import CaptureFixture, fixture

from tests.conftest import Fixture


@fixture
def test_flags() -> list[str]:
    return [
        "--send-quit",  # The game execution should finish after a single loop.
        "--no-resizeable",  # To deal with "no fast rendered" error
        "--no-scaled",  # To deal with "no fast rendered" error
    ]


@fixture(autouse=True)
def _assert_no_outputs(capfd: CaptureFixture[str]) -> Fixture[None]:
    yield
    _, err = capfd.readouterr()
    assert not err


def test_executable(
    zero_executable: Path,
    test_flags: list[str],
) -> None:
    # ruff: noqa: S603
    run([sys.executable, zero_executable, *test_flags], check=True)


def test_as_module(test_flags: list[str]) -> None:
    # ruff: noqa: S603
    run([sys.executable, "-m", "zero", *test_flags], check=True)
