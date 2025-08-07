from pytest import fixture, raises

from tests.utils import DummyPlatform, MockPlatform
from zero.core import Zero


@fixture
def zero(mock_platform: MockPlatform) -> Zero:
    return Zero(platform=mock_platform)


def test_zero() -> None:
    Zero(platform=DummyPlatform()).process_pending_commands()


def test_zero_process_command(zero: Zero) -> None:
    zero.process_pending_commands()


def test_zero_exit_command(zero: Zero, mock_platform: MockPlatform) -> None:
    assert not zero.is_exit_command
    zero.process_pending_commands()
    assert not zero.is_exit_command
    mock_platform.queue_exit_command()
    zero.process_pending_commands()
    assert zero.is_exit_command


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


def test_zero_loop_process_exit_command(
    zero: Zero, mock_platform: MockPlatform
) -> None:
    mock_platform.queue_exit_command()
    assert not zero.is_exit_command
    zero.loop()
    assert zero.is_exit_command


def test_zero_loop_until_exit_command(zero: Zero, mock_platform: MockPlatform) -> None:
    mock_platform.queue_exit_command()
    assert not zero.is_exit_command
    zero.loop_until_exit_command()
    assert zero.is_exit_command
