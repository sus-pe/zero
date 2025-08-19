from os import environ

import pytest
from pytest_asyncio import fixture

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
