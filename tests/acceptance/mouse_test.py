from collections.abc import Iterable

from pytest_asyncio import fixture

from tests.conftest import xfail
from zero.game import Game
from zero.mouse import MouseCursorMotion
from zero.type_wrappers.window import WindowXY


@fixture
async def stub_mouse_motions() -> Iterable[MouseCursorMotion]:
    return (
        MouseCursorMotion.from_xy(x=x, y=y)
        for x, y in zip(range(10), range(10), strict=True)
    )


@xfail(raises=AssertionError, strict=True)
async def test_mouse_cursor(
    game: Game, stub_mouse_motions: Iterable[MouseCursorMotion]
) -> None:
    for stub in stub_mouse_motions:
        game.send_mouse_motion(stub)
        await game.wait_for_next_mouse_motion()
        cursor = game.get_mouse_cursor_xy()
        assert cursor.xy == stub.xy
        window = game.get_window_view()
        cursor_sprite = game.get_mouse_cursor_sprite()
        assert not window.contains(
            cursor_sprite.as_np, at=WindowXY.from_xy(window.width, 0)
        )
        assert not window.contains(
            cursor_sprite.as_np, at=WindowXY.from_xy(0, window.height)
        )
        assert window.contains(cursor_sprite.as_np, at=cursor.xy)
