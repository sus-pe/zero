from collections.abc import AsyncGenerator
from typing import Any

from pytest_asyncio import fixture

from zero.game import Game
from zero.game_loader import GameLoader


@fixture
async def game() -> AsyncGenerator[Game, Any]:
    async with GameLoader() as game:
        yield game
