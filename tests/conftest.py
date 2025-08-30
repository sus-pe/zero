import tracemalloc
import warnings
from collections.abc import AsyncGenerator, Generator, Iterable
from os import environ
from pathlib import Path
from sys import platform

import pytest
from pytest import fixture

from zero.mouse import MouseCursorEvent
from zero.resources.loader import ResourceLoader
from zero.type_wrappers.arithmetic import Bit

type Fixture[T] = Generator[T, None, None]
type AsyncFixture[T] = AsyncGenerator[T, None]

parametrize = pytest.mark.parametrize
xfail = pytest.mark.xfail
raises = pytest.raises
slow = pytest.mark.slow


def pytest_sessionstart() -> None:
    tracemalloc.start(1000)


def pytest_configure() -> None:  # pragma: no cover
    if "CI" in environ and platform != "win32":
        warnings.filterwarnings(
            "ignore",
            message=r".*no fast renderer available.*",
        )


@fixture(scope="session", autouse=True)
def sdl_headless_env() -> None:
    # Must be set before pygame.init()
    environ.setdefault("SDL_VIDEODRIVER", "dummy")
    environ.setdefault("SDL_AUDIODRIVER", "dummy")


@fixture
def sdl_hw_videodriver() -> Fixture[str]:
    prev = environ.pop("SDL_VIDEODRIVER")
    yield "auto"
    environ.setdefault("SDL_VIDEODRIVER", prev)


@fixture
def resource_loader() -> ResourceLoader:
    return ResourceLoader()


@fixture(scope="session")
def project_root() -> Path:
    return Path(__file__).parent.parent.resolve()


@fixture(scope="session")
def dist_root(project_root: Path) -> Path:
    res = project_root / "dist"
    assert res.is_dir()
    return res


@fixture(scope="session")
def zero_executable(dist_root: Path) -> Path:
    matches = list(dist_root.glob("zero-*.whl"))
    assert matches, f"No zero-*.whl found in {dist_root}!"
    assert len(matches) == 1, "Supposed to be a single zero-*.whl!"
    wheel = matches[0]
    res = dist_root / wheel
    assert res.is_file()
    return res


@fixture
def stub_mouse_events() -> Iterable[MouseCursorEvent]:
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
