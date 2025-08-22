import sys
from pathlib import Path
from subprocess import run


def test_executable(zero_executable: Path) -> None:
    # ruff: noqa: S603
    run([sys.executable, zero_executable, "--send-quit"], check=True)


def test_as_module() -> None:
    # ruff: noqa: S603
    run([sys.executable, "-m", "zero", "--send-quit"], check=True)
