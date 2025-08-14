import pygame
import pytest

from zero.game import Game


@pytest.mark.xfail(strict=True)
async def test_mouse(game: Game) -> None:
    expected_mouse = Mouse(
        x=0,
        y=0,
        dx=1,
        dy=1,
        left=0,
        middle=0,
        right=0,
        # encode_fmt = {"pos": (x, y), "rel": (dx, dy), "buttons": (left, middle, right)}
    )

    pygame.event.post(
        pygame.event.Event(
            pygame.MOUSEMOTION,
            expected_mouse.encode_pygame(),
        )
    )

    mouse = await game.wait_next_mouse_event()
    assert mouse == expected_mouse
