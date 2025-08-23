from collections.abc import Iterable

from tests.conftest import parametrize
from zero.mouse import Mouse, MouseCursorEvent
from zero.type_wrappers.arithmetic import (
    Bit,
    LeftMouseBit,
    MiddleMouseBit,
    RightMouseBit,
)
from zero.type_wrappers.window import WindowXY


@parametrize(
    argnames="mouse",
    argvalues=[
        MouseCursorEvent(
            xy=WindowXY.from_xy(x=131509, y=9123),
            dx=-11324,
            dy=1123,
            left=LeftMouseBit(Bit.one),
            right=RightMouseBit(1),
            middle=MiddleMouseBit(0),
        ),
    ],
)
def test_mouse_basic(mouse: MouseCursorEvent) -> None:
    pygame_mouse = mouse.as_pygame()
    assert pygame_mouse == {
        "pos": (mouse.x, mouse.y),
        "rel": (mouse.dx, mouse.dy),
        "buttons": (mouse.left, mouse.middle, mouse.right),
    }

    assert mouse == MouseCursorEvent.from_pygame(pygame_mouse)
    assert mouse.as_pygame_event()
    assert mouse.xy == WindowXY.from_xy(*pygame_mouse["pos"])


def test_mouse_entity(stub_mouse_events: Iterable[MouseCursorEvent]) -> None:
    mouse_entity = Mouse()
    for stub in stub_mouse_events:
        mouse_entity.update(stub)
        assert mouse_entity.cursor_xy == stub.xy
        assert mouse_entity.left == stub.left
        assert mouse_entity.right == stub.right
        assert mouse_entity.middle == stub.middle
