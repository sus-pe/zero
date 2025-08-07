from abc import ABC
from collections.abc import Sequence
from typing import TypeAlias

from zero.core.types import PositiveInt


class Command(ABC):
    pass


class ExitCommand(Command):
    pass


CommandQueue: TypeAlias = Sequence[Command]


class Platform(ABC):
    def __init__(self) -> None:
        self._pending_commands: list[Command] = []

    def queue_exit_command(self) -> None:
        self._pending_commands.append(ExitCommand())

    def get_pending_commands(self) -> CommandQueue:
        """
        Asynchronously the platform aggregates pending commands.
        This returns all the commands that were not retrieved since the last call.
        """
        res = self._pending_commands.copy()
        self._pending_commands.clear()
        return res


class Zero:
    def __init__(self, platform: Platform) -> None:
        self.loop_counter = 0
        self.is_exit_command = False
        assert isinstance(platform, Platform)
        self._platform = platform

    def process_pending_commands(self) -> None:
        for command in self._platform.get_pending_commands():
            match command:
                case ExitCommand():
                    self.is_exit_command = True

    def loop(self) -> None:
        self.loop_counter += 1
        self.process_pending_commands()

    def loop_for(self, loops: PositiveInt) -> None:
        assert loops > 0

        for i in range(loops):
            self.loop()

    def loop_until_exit_command(self) -> None:
        while not self.is_exit_command:
            self.loop()
