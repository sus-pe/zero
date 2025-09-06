from abc import ABC, abstractmethod
from dataclasses import dataclass
from types import TracebackType
from typing import Any

from zero.logger import Logger


def assert_traceback_suffix(suffix: TracebackType, traceback: TracebackType) -> None:
    scanned: TracebackType | None = traceback
    while scanned:
        if scanned.tb_frame == suffix.tb_frame:
            return
        scanned = scanned.tb_next
    error_msg = f"Given {suffix=} is not a suffix of {traceback=}."
    raise AssertionError(error_msg)


@dataclass(frozen=True)
class ExceptionContext:
    exc_type: type[BaseException]  # exc_ prefix to not shadow builtin type
    value: BaseException
    traceback: TracebackType

    @classmethod
    def create_from(cls, e: BaseException) -> "ExceptionContext":
        assert e
        assert e.__traceback__
        return ExceptionContext(
            exc_type=type(e),
            value=e,
            traceback=e.__traceback__,
        )

    def assert_equals(self, e: BaseException) -> None:
        assert e

        assert isinstance(e, self.exc_type)

        assert e == self.value

        assert e.__traceback__
        assert_traceback_suffix(self.traceback, e.__traceback__)


type Log = tuple[str, Any, Any]


class Support(ABC):
    @abstractmethod
    def notify_crashed(self, reason: BaseException) -> None:
        """
        Notify if an unexpected exception is raised all the way back to entrypoint.
        """


class CompositeSupport(Support):
    def __init__(self, *support: Support) -> None:
        assert support is not None
        self._subscribers = support

    def notify_crashed(self, reason: BaseException) -> None:
        for sub in self._subscribers:
            sub.notify_crashed(reason)


class LoggerSupport(Support):
    def __init__(self, logger: Logger) -> None:
        self._logger = logger

    def notify_crashed(self, reason: BaseException) -> None:
        self._logger.critical(
            "Support notified of crash!", exc_info=ExceptionContext.create_from(reason)
        )
