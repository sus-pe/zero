from zero.type_wrappers.window import WindowXY


def test_window_xy() -> None:
    assert WindowXY.from_xy(0, 0) + WindowXY.from_xy(1, 1) == WindowXY.from_xy(1, 1)
