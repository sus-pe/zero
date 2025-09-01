import sys
from pathlib import Path

from pytest import fixture

from tests.acceptance.conftest import assert_subprocess
from tests.conftest import assert_dummy_sdl, skip_in_ci_if


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


@skip_in_ci_if(
    sys.platform != "win32",
    reason="Only Windows runner supports fast renderer at-the-moment.",
)
async def test_with_hw_rendered(test_flags: list[str], sdl_hw_videodriver: str) -> None:
    assert sdl_hw_videodriver != "dummy"
    test_flags.append("--is-scaled")
    await assert_module(test_flags)


async def test_with_no_fast_renderer_warning_suppressor(test_flags: list[str]) -> None:
    """
    In CI, ubuntu and macOS runners do not come out of the box with a fast video renderer.
    This causes CI jobs to fail when running with --is-scaled.
    I've decided I want CI to test --is-scaled, but I don't want to configure the runners with
    fast renderer, so I chose to instead implement a flag to disable this warning, which will only
    be used in CI.
    """
    assert_dummy_sdl()
    test_flags.append("--is-scaled")
    test_flags.append("--is-allow-no-fast-renderer")
    await assert_module(test_flags)
