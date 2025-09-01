from tests.conftest import raises
from zero.display import Display, DisplayConfig


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
