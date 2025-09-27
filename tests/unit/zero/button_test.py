from collections.abc import Iterator

from zero.game import Game
from zero.mouse import MouseCursorEvent


async def test_button(
    game: Game, stub_mouse_events: Iterator[MouseCursorEvent]
) -> None:
    for mouse in stub_mouse_events:
        game.add_button(at=mouse.xy)

        game.send_mouse_motion(mouse)
        await game.wait_for_next_mouse_motion()
