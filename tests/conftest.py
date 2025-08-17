from os import environ

import pytest
from pytest_asyncio import fixture

parametrize = pytest.mark.parametrize
xfail = pytest.mark.xfail


@fixture(scope="session", autouse=True)
async def sdl_headless_env() -> None:
    # Must be set before pygame.init()
    environ.setdefault("SDL_VIDEODRIVER", "dummy")
