import asyncio
import sys

import pygame
from pygame import Clock


def main() -> int:  # pragma: no cover
    asyncio.run(open_and_close_window(asyncio.Event()))
    return 0


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())


async def open_and_close_window(is_started_event: asyncio.Event, fps: int = 60) -> None:
    assert fps > 0

    pygame.init()
    try:
        await setup_display()
        await game_loop_until_quit(is_started_event, fps)
    finally:
        pygame.quit()


async def game_loop_until_quit(is_started_event: asyncio.Event, fps: int) -> None:
    assert fps > 0
    assert not is_started_event.is_set()

    running = True
    clock: Clock = pygame.time.Clock()
    is_started_event.set()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.display.flip()

        await asyncio.sleep(0)
        clock.tick(fps)


async def setup_display() -> None:
    pygame.display.set_mode((640, 480))
    pygame.display.set_caption("Automated Test Window")
