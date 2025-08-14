import logging
from asyncio import Event, Queue, Task, create_task, sleep
from types import TracebackType

import pygame
from pygame import Clock, Surface

from zero.contextmanagers import CONTEXT_MANAGER_EXIT_DO_NOT_SUPPRESS_EXCEPTION

logger = logging.getLogger(__name__)


class ResizeEvent:
    width: float
    height: float


class Game:
    def __init__(self) -> None:
        self._resize_event_queue: Queue[ResizeEvent] = Queue()
        self._is_quit_event: Event = Event()
        self._window_task: Task[None] | None = None
        self._is_started_event: Event = Event()
        self._fps: int = 240

    async def __aenter__(self) -> "Game":
        self._window_task = create_task(
            self.start_game(),
        )
        await self._is_started_event.wait()
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> bool | None:
        assert self._is_started_event.is_set()
        assert self._window_task is not None
        await self.try_send_quit()
        await self.wait_exit()
        await self._window_task
        self._is_quit_event.set()
        return CONTEXT_MANAGER_EXIT_DO_NOT_SUPPRESS_EXCEPTION

    async def wait_exit(self) -> None:
        await self._is_quit_event.wait()

    async def setup_display(self) -> None:
        pygame.display.set_mode((640, 480), pygame.RESIZABLE)
        pygame.display.set_caption("Automated Test Window")

    async def game_loop_until_quit(self) -> None:
        assert self._fps > 0
        assert not self._is_started_event.is_set()

        running = True
        clock: Clock = pygame.time.Clock()
        self._is_started_event.set()
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            pygame.display.flip()

            # yield event loop
            await sleep(0)
            clock.tick(self._fps)

    async def start_game(self) -> None:
        assert not self._is_quit_event.is_set()
        assert not self._is_started_event.is_set()
        pygame.init()
        try:
            await self.setup_display()
            self.assert_resizeable()
            await self.game_loop_until_quit()
        finally:
            pygame.quit()
            assert not self._is_quit_event.is_set()
            self._is_quit_event.set()

    async def send_quit(self) -> None:
        pygame.event.post(pygame.event.Event(pygame.QUIT))

    async def try_send_quit(self) -> None:
        try:
            await self.send_quit()
        except pygame.error as e:
            logger.debug("caught %s", e, exc_info=e)

    def assert_get_display_surface(self) -> Surface:
        surface: Surface | None = pygame.display.get_surface()
        assert surface
        return surface

    def assert_resizeable(self) -> None:
        assert self.is_display_resizeable()

    def is_display_resizeable(self) -> bool:
        return bool(self.get_display_flags() & pygame.RESIZABLE)

    def get_display_flags(self) -> int:
        return self.assert_get_display_surface().get_flags()
