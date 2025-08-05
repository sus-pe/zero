from abc import ABC, abstractmethod
from typing import Collection


class Command(ABC):
    pass


class NullCommand(Command):
    pass


class Platform(ABC):
    @abstractmethod
    def get_pending_commands(self) -> Collection[Command]:
        """
        Asynchronously the platform aggregates pending commands.
        This returns all the commands that were not retrieved since the last call.
        """


class Zero:
    def __init__(self, platform: Platform):
        self.is_exit_command = False
        assert isinstance(platform, Platform)
        self._platform = platform

    def process_pending_commands(self):
        self._platform.get_pending_commands()
