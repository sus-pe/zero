from tests.conftest import parametrize
from zero.mouse import MouseCursor, MouseCursorMotion
from zero.type_wrappers.arithmetic import (
    Bit,
    LeftMouseBit,
    MiddleMouseBit,
    RightMouseBit,
    WindowXY,
)


@parametrize(
    argnames="mouse",
    argvalues=[
        MouseCursorMotion(
            cursor=MouseCursor.from_xy(x=131509, y=9123),
            dx=-11324,
            dy=1123,
            left=LeftMouseBit(Bit.one),
            right=RightMouseBit(1),
            middle=MiddleMouseBit(0),
        ),
    ],
)
def test_mouse_basic(mouse: MouseCursorMotion) -> None:
    pygame_mouse = mouse.as_pygame()
    assert pygame_mouse == {
        "pos": (mouse.x, mouse.y),
        "rel": (mouse.dx, mouse.dy),
        "buttons": (mouse.left, mouse.middle, mouse.right),
    }

    assert mouse == MouseCursorMotion.from_pygame(pygame_mouse)
    assert mouse.as_pygame_event()
    assert mouse.cursor.xy == WindowXY.from_xy(*pygame_mouse["pos"])


def test_mouse_cursor() -> None:
    MouseCursor.from_xy(x=0, y=0)
