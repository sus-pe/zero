from collections.abc import AsyncGenerator
from typing import Any

from pytest_asyncio import fixture

from zero.game import Game


@fixture
async def game() -> AsyncGenerator[Game, Any]:
    async with Game() as game:
        yield game
