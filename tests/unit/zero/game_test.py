from collections.abc import Iterable

from zero.game import Game
from zero.mouse import MouseCursorEvent


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


async def test_mouse_cursor_out_of_boundary(
    game: Game, stub_mouse_events: Iterable[MouseCursorEvent]
) -> None:
    for stub in stub_mouse_events:
        event = stub.as_pygame_event()
        event.dict["pos"] = tuple(-1 * c for c in event.dict["pos"])
        game.send(event)
        await game.wait_next_loop()
