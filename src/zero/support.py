from abc import ABC, abstractmethod

from zero.logger import Logger


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
        pass

    def notify_crashed(self, reason: BaseException) -> None:
        """
        #TODO - iomplement this
        """
