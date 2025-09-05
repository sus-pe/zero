from tests.conftest import raises
from zero import __main__
from zero.game import Game
from zero.game_loader import GameLoaderPostLoadPlugin


class AlwaysFailError(Exception):
    pass


class AlwaysFailPostLoadPlugin(GameLoaderPostLoadPlugin):
    async def send_commands(self, game: Game) -> None:
        assert game, "Supposed to be initialized!"
        raise AlwaysFailError


async def test_sanity() -> None:
    await __main__.main_test()


async def test_post_load_plugin_failure() -> None:
    with raises(AlwaysFailError):
        await __main__.main_test(post_load_plugin=AlwaysFailPostLoadPlugin())
