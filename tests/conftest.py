from os import environ
from pathlib import Path

import pytest
from pytest_asyncio import fixture

from zero.global_config import (
    DIST_NAME,
    ONEFILE_ARTIFACT_EXECUTABLE_NAME,
)
from zero.resources.loader import ResourceLoader

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
    res = project_root / DIST_NAME
    assert res.is_dir()
    return res


@fixture(scope="session")
async def zero_executable(dist_root: Path) -> Path:
    res = dist_root / ONEFILE_ARTIFACT_EXECUTABLE_NAME
    assert res.is_file()
    return res
