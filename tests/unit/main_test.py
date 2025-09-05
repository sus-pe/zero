from tests.conftest import fixture, raises
from zero import __main__
from zero.game import Game
from zero.game_loader import GameLoaderPostLoadPlugin
from zero.support import Support


class AlwaysFailError(Exception):
    pass


class AlwaysFailPostLoadPlugin(GameLoaderPostLoadPlugin):
    async def send_commands(self, game: Game) -> None:
        assert game, "Supposed to be initialized!"
        raise AlwaysFailError


class MockSupport(Support):
    def __init__(self) -> None:
        self._crashed: BaseException | None = None

    def notify_crashed(self, reason: BaseException) -> None:
        assert not self._crashed
        self._crashed = reason

    def assert_not_crashed(self) -> None:
        assert not self._crashed

    def assert_crashed(self, reason: type[BaseException]) -> None:
        assert self._crashed
        assert isinstance(self._crashed, reason)


@fixture
def mock_support() -> MockSupport:
    return MockSupport()


async def test_sanity(mock_support: MockSupport) -> None:
    await __main__.main_test(support=mock_support)
    mock_support.assert_not_crashed()


async def test_post_load_plugin_failure(mock_support: MockSupport) -> None:
    with raises(AlwaysFailError):
        await __main__.main_test(
            support=mock_support, post_load_plugin=AlwaysFailPostLoadPlugin()
        )
    mock_support.assert_crashed(AlwaysFailError)
