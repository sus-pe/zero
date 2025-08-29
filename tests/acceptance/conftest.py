import locale
from asyncio import create_subprocess_exec
from asyncio.subprocess import PIPE

from pytest import CaptureFixture, fixture

from tests.conftest import Fixture

ENC = locale.getpreferredencoding(do_setlocale=False)


@fixture(autouse=True)
def _assert_no_outputs(capfd: CaptureFixture[str]) -> Fixture[None]:
    yield
    _, err = capfd.readouterr()
    assert not err


async def assert_subprocess(command: str, flags: list[str]) -> None:
    proc = await create_subprocess_exec(
        command,
        *flags,
        stdout=PIPE,
        stderr=PIPE,
    )
    _, raw_stderr = await proc.communicate()
    stderr = raw_stderr.decode(ENC)
    assert not stderr, stderr
    assert proc.returncode == 0
