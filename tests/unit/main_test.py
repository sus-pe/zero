from typing import Any

from tests.conftest import fixture, raises
from zero import __main__
from zero.game import Game
from zero.game_loader import GameLoaderPostLoadPlugin
from zero.logger import Logger
from zero.support import (
    ExceptionContext,
    LoggerSupport,
    Support,
    assert_traceback_suffix,
)


class AlwaysFailError(Exception):
    pass


class AlwaysFailPostLoadPlugin(GameLoaderPostLoadPlugin):
    async def send_commands(self, game: Game) -> None:
        assert game, "Supposed to be initialized!"
        raise AlwaysFailError


class MockSupport(Support):
    def __init__(self) -> None:
        self.crash_reason: ExceptionContext | None = None

    def notify_crashed(self, reason: BaseException) -> None:
        assert not self.crash_reason
        self.crash_reason = ExceptionContext.create_from(reason)

    def assert_not_crashed(self) -> None:
        assert not self.crash_reason

    def assert_crashed(self, reason: BaseException) -> None:
        assert self.crash_reason
        self.crash_reason.assert_equals(reason)


class MockLogger(Logger):
    def __init__(self) -> None:
        self._exc_context: ExceptionContext | None = None

    def critical(self, msg: str, *args: Any, **kwargs: Any) -> None:  # noqa: ANN401
        assert "exc_info" in kwargs
        assert not args
        assert msg
        self._exc_context = kwargs["exc_info"]

    def assert_logged_critical(self, e: BaseException) -> None:
        assert self._exc_context

        assert isinstance(e, self._exc_context.exc_type)

        assert e == self._exc_context.value

        assert e.__traceback__
        assert_traceback_suffix(self._exc_context.traceback, e.__traceback__)


class MockLoggerSupport(LoggerSupport):
    def __init__(self, logger: MockLogger) -> None:
        super().__init__(logger)
        self._logger: MockLogger = logger

    def assert_logged_critical(self, e: BaseException) -> None:
        self._logger.assert_logged_critical(e)


@fixture
def mock_support() -> MockSupport:
    return MockSupport()


async def test_sanity(mock_support: MockSupport) -> None:
    await __main__.main_test(support=mock_support)
    mock_support.assert_not_crashed()


@fixture
def always_fail_plugin() -> AlwaysFailPostLoadPlugin:
    return AlwaysFailPostLoadPlugin()


async def test_post_load_plugin_failure(
    mock_support: MockSupport, always_fail_plugin: AlwaysFailPostLoadPlugin
) -> None:
    with raises(AlwaysFailError) as e:
        await __main__.main_test(
            support=mock_support, post_load_plugin=always_fail_plugin
        )
    mock_support.assert_crashed(e.value)


@fixture
def mock_logger() -> MockLogger:
    return MockLogger()


@fixture
def mock_logger_support(mock_logger: MockLogger) -> MockLoggerSupport:
    return MockLoggerSupport(mock_logger)


async def test_logger_support(
    mock_logger_support: MockLoggerSupport, always_fail_plugin: AlwaysFailPostLoadPlugin
) -> None:
    with raises(AlwaysFailError) as e:
        await __main__.main_test(
            support=mock_logger_support, post_load_plugin=always_fail_plugin
        )
    mock_logger_support.assert_logged_critical(e.value)


def always_raise(e: BaseException | type[BaseException]) -> None:
    raise e


def always_reraise(
    mock_support: MockSupport, e: BaseException | type[BaseException]
) -> None:
    try:
        always_raise(e)
    except BaseException as exc:
        mock_support.notify_crashed(exc)
        raise


def test_assert_traceback_suffix(mock_support: MockSupport) -> None:
    with raises(AlwaysFailError) as e:
        always_reraise(mock_support, AlwaysFailError)

    mock_support.assert_crashed(e.value)

    assert mock_support.crash_reason
    notified_traceback = mock_support.crash_reason.traceback

    assert_traceback_suffix(suffix=notified_traceback, traceback=e.tb)

    with raises(AssertionError):
        assert_traceback_suffix(suffix=e.tb, traceback=notified_traceback)
