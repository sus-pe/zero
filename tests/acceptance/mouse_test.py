from pytest import fixture

from zero.game import Game
from zero.mouse import MouseMotion


@fixture
def stub_mouse_motion() -> MouseMotion:
    return MouseMotion.from_xy(x=0, y=0)


async def test_mouse(game: Game, stub_mouse_motion: MouseMotion) -> None:
    game.send_mouse_motion(stub_mouse_motion)

    mouse = await game.wait_for_next_mouse_motion()
    assert mouse == stub_mouse_motion
