import sys
from pathlib import Path

from pytest import fixture

from tests.acceptance.conftest import assert_subprocess


@fixture
def test_flags() -> list[str]:
    return ["--is-test", "--no-is-scaled"]


async def test_executable(
    zero_executable: Path,
    test_flags: list[str],
) -> None:
    test_flags.insert(0, str(zero_executable))
    await assert_subprocess(sys.executable, test_flags)


async def assert_module(flags: list[str]) -> None:
    await assert_subprocess(
        sys.executable,
        flags=["-m", "zero", *flags],
    )


async def test_as_module(test_flags: list[str]) -> None:
    await assert_module(test_flags)


async def test_with_hw_rendered(
    test_flags: list[str], sdl_hw_videodriver: "str"
) -> None:
    assert sdl_hw_videodriver != "dummy"
    test_flags.append("--is-scaled")
    await assert_module(test_flags)
