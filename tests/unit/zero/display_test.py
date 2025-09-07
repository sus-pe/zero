from tests.conftest import raises
from zero.display import Display, DisplayConfig
from zero.type_wrappers.arithmetic import NotPositiveIntError, Pixels
from zero.type_wrappers.window import WindowXY


def test_game_display_fullscreen(display: Display) -> None:
    display = display.as_windowed
    assert display.is_windowed
    display = display.as_windowed
    assert display.is_windowed
    display = display.as_fullscreen
    assert display.is_fullscreen
    display = display.as_fullscreen
    assert display.is_fullscreen
    display = display.toggled_fullscreen
    assert display.is_windowed
    display = display.toggled_fullscreen
    assert display.is_fullscreen


def test_display_config_disallow_fast_renderer() -> None:
    with raises(AssertionError, match=DisplayConfig.SLOW_RENDERER_ERROR_MSG):
        DisplayConfig(
            is_scaled=True,
            is_hidden=True,
            is_fullscreen=True,
            is_allow_no_fast_renderer=False,
        )


def test_clamp_to_display(display: Display) -> None:
    neg_x, neg_y = -1, -1
    pos_x, pos_y = 1, 1

    assert display.origin == display.clamp(display.origin)
    assert display.origin == display.clamp((neg_x, neg_y))

    assert WindowXY.from_xy(pos_x, 0) == display.clamp((pos_x, neg_y))
    assert WindowXY.from_xy(0, pos_y) == display.clamp((neg_x, pos_y))

    assert WindowXY.from_xy(pos_x, pos_y) == display.clamp((pos_x, pos_y))

    assert display.max_xy == display.clamp(display.resolution.tuple)


def test_pixels_must_be_positive() -> None:
    Pixels(1)

    with raises(NotPositiveIntError):
        Pixels(0)

    with raises(NotPositiveIntError):
        Pixels(-1)
