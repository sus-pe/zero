from logging import Logger as _Logger
from logging import getLogger
from typing import Any, Protocol


class Logger(Protocol):
    def critical(self, msg: str, *args: Any, **kwargs: Any) -> None: ...  # noqa: ANN401


def create_for(name: str) -> _Logger:
    return getLogger(name)
