from pytest import fixture, raises

from tests.utils import MockPlatform
from zero.core import DisplaySettings, Zero
from zero.core.types import DisplayResolution


@fixture
def display_resolution() -> DisplayResolution:
    return DisplayResolution.SD_4_3


@fixture
def zero(mock_platform: MockPlatform, display_resolution: DisplayResolution) -> Zero:
    return Zero(platform=mock_platform, display_resolution=display_resolution.value)


def test_zero_loop(zero: Zero) -> None:
    assert zero.loop_counter == 0
    zero.loop()
    assert zero.loop_counter == 1


def test_zero_loop_for_errors(zero: Zero) -> None:
    with raises(AssertionError):
        zero.loop_for(-3)

    with raises(AssertionError):
        zero.loop_for(0)


def test_zero_loop_for(zero: Zero) -> None:
    loops = 20
    zero.loop_for(loops)
    assert zero.loop_counter == loops


def test_zero_loop_until_exit_command(zero: Zero, mock_platform: MockPlatform) -> None:
    mock_platform.queue_exit_command()
    assert not zero.is_exit_command
    zero.loop_until_exit_command()
    assert zero.is_exit_command


def test_zero_starts_window_on_first_loop(
    zero: Zero,
    mock_platform: MockPlatform,
) -> None:
    assert mock_platform.get_display_settings() is None
    zero.display_init()
    assert mock_platform.get_display_settings() is not None
    assert isinstance(mock_platform.get_display_settings(), DisplaySettings)
