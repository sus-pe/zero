import pygame

from zero.game import Game
from zero.mouse import MouseMotion


async def test_mouse(game: Game) -> None:
    expected_mouse = MouseMotion.from_xy(x=0, y=0)
    pygame.event.post(expected_mouse.as_pygame_event())

    mouse = await game.wait_for_next_mouse_motion()
    assert mouse == expected_mouse
