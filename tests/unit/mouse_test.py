from zero.mouse import MouseMotion


def test_mouse_basic() -> None:
    mouse = MouseMotion.parse(x=0, y=0)
    pygame_mouse = mouse.as_pygame()
    assert pygame_mouse == {
        "pos": (mouse.x, mouse.y),
        "rel": (mouse.dx, mouse.dy),
        "buttons": (mouse.left, mouse.middle, mouse.right),
    }
