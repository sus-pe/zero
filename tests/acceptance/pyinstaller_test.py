from pathlib import Path
from subprocess import run


def test_pyinstaller(zero_executable: Path) -> None:
    # ruff: noqa: S603
    run([zero_executable, "--send-quit"], check=True)
