from tests.conftest import parametrize
from zero.mouse import MouseMotion
from zero.type_wrappers.arithmetic import (
    Bit,
    LeftMouseBit,
    MiddleMouseBit,
    RightMouseBit,
    WindowX,
    WindowY,
)


@parametrize(
    argnames="mouse",
    argvalues=[
        MouseMotion.from_xy(x=0, y=0),
        MouseMotion(
            x=WindowX(0),
            y=WindowY(0),
            dx=-1,
            dy=1,
            left=LeftMouseBit(Bit.one),
            right=RightMouseBit(1),
            middle=MiddleMouseBit(0),
        ),
    ],
)
def test_mouse_basic(mouse: MouseMotion) -> None:
    pygame_mouse = mouse.as_pygame()
    assert pygame_mouse == {
        "pos": (mouse.x, mouse.y),
        "rel": (mouse.dx, mouse.dy),
        "buttons": (mouse.left, mouse.middle, mouse.right),
    }

    assert mouse == MouseMotion.from_pygame(pygame_mouse)
    assert mouse.as_pygame_event()
