from zero.core import IO, GameLoop


def test_zero_loop_until_exit_command(zero: GameLoop, io: IO) -> None:
    io.queue_exit_command()
    assert not zero.is_exit_command
    zero.loop_until_exit_command()
    assert zero.is_exit_command
