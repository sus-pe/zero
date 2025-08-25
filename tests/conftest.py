from collections.abc import Iterable
from os import environ
from pathlib import Path

import pytest
from pytest_asyncio import fixture

from zero.mouse import MouseCursorEvent
from zero.resources.loader import ResourceLoader
from zero.type_wrappers.arithmetic import Bit

parametrize = pytest.mark.parametrize
xfail = pytest.mark.xfail


@fixture(scope="session", autouse=True)
async def sdl_headless_env() -> None:
    # Must be set before pygame.init()
    environ.setdefault("SDL_VIDEODRIVER", "dummy")


@fixture
async def resource_loader() -> ResourceLoader:
    return ResourceLoader()


@fixture(scope="session")
async def project_root() -> Path:
    return Path(__file__).parent.parent.resolve()


@fixture(scope="session")
async def dist_root(project_root: Path) -> Path:
    res = project_root / "dist"
    assert res.is_dir()
    return res


@fixture(scope="session")
async def zero_executable(dist_root: Path) -> Path:
    matches = list(dist_root.glob("zero-*.whl"))
    assert matches, f"No zero-*.whl found in {dist_root}!"
    assert len(matches) == 1, "Supposed to be a single zero-*.whl!"
    wheel = matches[0]
    res = dist_root / wheel
    assert res.is_file()
    return res


@fixture
async def stub_mouse_events() -> Iterable[MouseCursorEvent]:
    return (
        MouseCursorEvent.from_xy(x=x, y=y, left=left, middle=middle, right=right)
        for x, y, left, middle, right in zip(
            range(10),
            range(10),
            Bit.alternating(10),
            Bit.alternating(10),
            Bit.alternating(10),
            strict=True,
        )
    )
