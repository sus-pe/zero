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
        recieved = await game.wait_for_next_mouse_motion()
        assert isinstance(recieved, MouseCursorEvent)
        assert recieved == stub
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
    # TODO: Cleanup this test
    for stub in stub_mouse_events:
        event = stub.as_pygame_event()
        event.dict["pos"] = tuple(-1 * c for c in event.dict["pos"])
        game.send(event)
        recieved = await game.wait_for_next_mouse_motion()
        assert isinstance(recieved, MouseCursorEvent)
        assert recieved.xy == game.display.origin
        await game.wait_next_loop()
        assert game.get_mouse_cursor_xy() == game.display.origin

        event = stub.as_pygame_event()
        event.dict["pos"] = tuple(
            c + s
            for c, s in zip(event.dict["pos"], game.display.resolution, strict=True)
        )
        assert event.dict["pos"][0] > game.display.resolution.max_x
        assert event.dict["pos"][1] > game.display.resolution.max_y

        game.send(event)
        recieved = await game.wait_for_next_mouse_motion()
        assert isinstance(recieved, MouseCursorEvent)
        assert recieved.xy == game.display.max_xy
        await game.wait_next_loop()
        assert game.get_mouse_cursor_xy() == game.display.max_xy
