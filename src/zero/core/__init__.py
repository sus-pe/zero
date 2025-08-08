from abc import ABC
from collections.abc import Sequence
from dataclasses import dataclass

from zero.core.types import PositiveInt, Resolution


class Command(ABC):
    pass


class ExitCommand(Command):
    pass


type CommandQueue = Sequence[Command]


@dataclass(frozen=True)
class DisplaySettings:
    resolution: Resolution


class Platform(ABC):
    def __init__(self) -> None:
        self._pending_commands: list[Command] = []
        self.display: DisplaySettings | None = None

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

    def get_display_settings(self) -> DisplaySettings | None:
        return self.display

    def set_display_settings(self, display: DisplaySettings) -> None:
        self.display = display


class Zero:
    def __init__(
        self,
        platform: Platform,
        display_resolution: Resolution,
    ) -> None:
        self.display_resolution = display_resolution
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

        for _i in range(loops):
            self.loop()

    def loop_until_exit_command(self) -> None:
        while not self.is_exit_command:
            self.loop()

    def display_init(self) -> None:
        self._platform.set_display_settings(DisplaySettings(self.display_resolution))
