from pytest import fixture

from tests.conftest import AsyncFixture
from zero.display import Display, DisplayConfig
from zero.game import Game
from zero.game_loader import GameLoader


@fixture
def display_config() -> DisplayConfig:
    return DisplayConfig(
        is_scaled=False,
        is_hidden=True,
        is_fullscreen=True,
    )


@fixture
def display(display_config: DisplayConfig) -> Display:
    return Display(display_config)


@fixture
async def game(display_config: DisplayConfig) -> AsyncFixture[Game]:
    # Scaled disabled to avoid "no-fast-render" errors.
    async with GameLoader(display_config) as game:
        yield game
