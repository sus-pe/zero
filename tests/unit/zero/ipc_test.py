import locale
import sys
from asyncio import create_subprocess_exec
from asyncio.subprocess import PIPE
from dataclasses import dataclass
from functools import cached_property
from typing import ClassVar


@dataclass(frozen=True)
class ProcessResult:
    raw_stdout: bytes
    raw_stderr: bytes
    raw_exit_code: int

    @cached_property
    def stdout(self) -> str:
        return self.raw_stdout.decode(self.ENC)

    @cached_property
    def stderr(self) -> str:
        return self.raw_stderr.decode(self.ENC)

    @cached_property
    def exit_code(self) -> int:
        res = self.raw_exit_code
        # Windows wraps negatives into unsigned 32-bit
        if self.raw_exit_code > 2**31:
            res -= 2**32
        return res

    ENC: ClassVar[str] = locale.getpreferredencoding(do_setlocale=False)


async def python_subprocess(*args: str) -> ProcessResult:
    # TODO: DUP(1)
    proc = await create_subprocess_exec(
        sys.executable,
        *args,
        stdout=PIPE,
        stderr=PIPE,
    )
    raw_stdout, raw_stderr = await proc.communicate()
    assert proc.returncode is not None

    return ProcessResult(
        raw_stdout=raw_stdout,
        raw_stderr=raw_stderr,
        raw_exit_code=proc.returncode,
    )


async def test_ipc() -> None:
    # TODO: Cleaup this test
    stdout = r"\nHello, world!\nSecond line!!!\n\n\n"
    stderr = r"\nHello, stderr!\r\nSecond is the gbest!!\n\r\n\r\n\n"
    exit_code = -134
    result: ProcessResult = await python_subprocess(
        "-c",
        f"import sys; sys.stderr.write(r'{stderr}'); sys.stdout.write(r'{stdout}'); exit({exit_code})",
    )

    assert result.exit_code == exit_code
    assert result.stderr == stderr
    assert result.stdout == stdout
