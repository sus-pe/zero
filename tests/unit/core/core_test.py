from pytest import fixture

from zero.core import IO, DisplaySettings, GameLoop
from zero.core.types import DisplayResolution


@fixture
def display_resolution() -> DisplayResolution:
    return DisplayResolution.SD_4_3


@fixture
def display_settings(display_resolution: DisplayResolution) -> DisplaySettings:
    return DisplaySettings(display_resolution.value)


@fixture
def zero(io: IO) -> GameLoop:
    return GameLoop(io=io)


def test_zero_loop_until_exit_command(zero: GameLoop, io: IO) -> None:
    io.queue_exit_command()
    assert not zero.is_exit_command
    zero.loop_until_exit_command()
    assert zero.is_exit_command


def test_zero_starts_window_on_first_loop(
    display_settings: DisplaySettings,
    io: IO,
) -> None:
    assert io.get_display_settings() is None
    io.set_display_settings(display_settings)
    assert io.get_display_settings() is display_settings
