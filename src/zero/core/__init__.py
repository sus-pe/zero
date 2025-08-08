from abc import ABC
from collections.abc import Sequence
from dataclasses import dataclass

from zero.core.types import DisplayResolution


class Command(ABC):
    pass


class ExitCommand(Command):
    pass


type CommandQueue = Sequence[Command]


@dataclass(frozen=True)
class DisplaySettings:
    resolution: DisplayResolution


class IO:
    def __init__(self, display_settings: DisplaySettings) -> None:
        self._pending_commands: list[Command] = []
        self._display_settings = display_settings

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


class GameLoop:
    def __init__(
        self,
        io: IO,
    ) -> None:
        self.loop_counter = 0
        self.is_exit_command = False
        self._io = io

    def process_pending_commands(self) -> None:
        for command in self._io.get_pending_commands():
            match command:
                case ExitCommand():
                    self.is_exit_command = True

    def loop(self) -> None:
        self.loop_counter += 1
        self.process_pending_commands()

    def loop_until_exit_command(self) -> None:
        while not self.is_exit_command:
            self.loop()
