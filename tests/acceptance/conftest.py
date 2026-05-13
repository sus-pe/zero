import locale
import sys
from asyncio import create_subprocess_exec
from asyncio.subprocess import PIPE
from pathlib import Path

import uv
from pytest import CaptureFixture, fixture

from tests.conftest import Fixture, fixture

ENC = locale.getpreferredencoding(do_setlocale=False)


@fixture(autouse=True)
def _assert_no_outputs(capfd: CaptureFixture[str]) -> Fixture[None]:
    yield
    _, err = capfd.readouterr()
    assert not err


async def assert_subprocess(command: str, flags: list[str], check_stderr: bool = True) -> None:
    proc = await create_subprocess_exec(
        command,
        *flags,
        stdout=PIPE,
        stderr=PIPE,
    )
    _, raw_stderr = await proc.communicate()
    if check_stderr:
        stderr = raw_stderr.decode(ENC)
        assert not stderr, stderr
    assert proc.returncode == 0


@fixture(scope="session")
async def zero_build_root(project_root: Path) -> Path:
    await assert_subprocess(uv.find_uv_bin(), ["build"], check_stderr=False)
    res = project_root / "dist"
    assert res.is_dir()
    return res


@fixture(scope="session")
def zero_executable(zero_build_root: Path) -> Path:
    matches = list(zero_build_root.glob("zero-*.whl"))
    assert matches, f"No zero-*.whl found in {zero_build_root}!"
    assert len(matches) == 1, "Supposed to be a single zero-*.whl!"
    wheel = matches[0]
    res = zero_build_root / wheel
    assert res.is_file()
    return res
