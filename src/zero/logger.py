from logging import Logger as _Logger
from logging import getLogger
from typing import Protocol


class Logger(Protocol):
    pass


def create_for(name: str) -> _Logger:
    return getLogger(name)
