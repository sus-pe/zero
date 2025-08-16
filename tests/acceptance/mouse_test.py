from collections.abc import Iterable

from pytest_asyncio import fixture

from tests.conftest import xfail
from zero.game import Game
from zero.mouse import MouseCursorMotion


@fixture
async def stub_mouse_motions() -> Iterable[MouseCursorMotion]:
    return (
        MouseCursorMotion.from_xy(x=x, y=y)
        for x, y in zip(range(10), range(10), strict=True)
    )


async def test_mouse(
    game: Game, stub_mouse_motions: Iterable[MouseCursorMotion]
) -> None:
    for stub in stub_mouse_motions:
        game.send_mouse_motion(stub)

        mouse = await game.wait_for_next_mouse_motion()
        assert mouse == stub


@xfail(strict=True)
async def test_mouse_cursor(
    game: Game, stub_mouse_motions: Iterable[MouseCursorMotion]
) -> None:
    for stub in stub_mouse_motions:
        game.send_mouse_motion(stub)
        await game.wait_for_next_mouse_motion()
        cursor = game.get_mouse_cursor()
        assert cursor.xy == stub.xy

        game.get_window_pixels()
