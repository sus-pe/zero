from pytest import fixture

from tests.conftest import AsyncFixture, Fixture
from zero.contextmanagers import PygameContext
from zero.display import Display, DisplayConfig
from zero.game import Game
from zero.game_loader import GameLoader


@fixture
def display_config() -> DisplayConfig:
    return DisplayConfig(
        is_scaled=False,
        is_hidden=True,
        is_fullscreen=True,
        is_allow_no_fast_renderer=False,
    )


@fixture
def pygame_context() -> Fixture[PygameContext]:
    with PygameContext() as ctx:
        yield ctx


@fixture
def display(display_config: DisplayConfig, pygame_context: PygameContext) -> Display:
    pygame_context.assert_init()
    return Display(display_config)


@fixture
async def game(
    display_config: DisplayConfig, pygame_context: PygameContext
) -> AsyncFixture[Game]:
    async with GameLoader(
        display_config=display_config, pygame_context=pygame_context
    ) as game:
        yield game
