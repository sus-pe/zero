from collections.abc import AsyncGenerator
from typing import Any

from pytest_asyncio import fixture

from zero.game import Game


@fixture
async def game() -> AsyncGenerator[Game, Any]:
    async with Game() as game:
        yield game


async def test_window_auto_with_event_driven(game: Game) -> None:
    await game.send_quit()
    await game.wait_exit()
