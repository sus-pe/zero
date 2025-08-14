from collections.abc import AsyncGenerator
from os import environ
from typing import Any

from pytest_asyncio import fixture

from zero.game import Game


@fixture(scope="session", autouse=True)
async def sdl_headless_env() -> None:
    # Must be set before pygame.init()
    environ.setdefault("SDL_VIDEODRIVER", "dummy")


@fixture
async def game() -> AsyncGenerator[Game, Any]:
    async with Game() as game:
        yield game
