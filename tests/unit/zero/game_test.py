from collections.abc import Iterable

from zero.display import Display
from zero.game import Game
from zero.mouse import MouseCursorEvent


async def test_game_display_fullscreen(display: Display) -> None:
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


async def test_game_fullscreen_button(game: Game) -> None:
    initial_state = game.display.is_fullscreen
    game.send_f11()
    await game.wait_next_loop()
    assert initial_state != game.display.is_fullscreen
    game.send_f11()
    await game.wait_next_loop()
    assert initial_state == game.display.is_fullscreen


async def test_mouse_cursor(
    game: Game, stub_mouse_events: Iterable[MouseCursorEvent]
) -> None:
    assert game.is_os_cursor_hidden()
    for stub in stub_mouse_events:
        game.send_mouse_motion(stub)
        await game.wait_for_next_mouse_motion()
        await game.wait_next_loop()
        cursor = game.get_mouse_cursor_xy()
        assert cursor == stub.xy
        if not stub.left:
            assert game.is_displayed(game.mouse_cursor_sprite, cursor)
        else:
            assert game.is_displayed(game.mouse_cursor_pressed_sprite, cursor)
