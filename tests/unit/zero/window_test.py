from zero.type_wrappers.window import WindowXY


def test_window_xy() -> None:
    assert WindowXY.from_xy(0, 0) + WindowXY.from_xy(1, 1) == WindowXY.from_xy(1, 1)


def test_window_xy_negated() -> None:
    origin = WindowXY.from_xy(0, 0)
    assert origin.negated == origin

    x, y = 1, 1
    window = WindowXY.from_xy(x, y)
    assert window.negated == (-x, -y)
