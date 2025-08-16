import logging
from asyncio import Event, Future, Queue, Task, create_task, sleep
from types import TracebackType
from typing import cast

import pygame
from pygame import Clock, Surface

from zero.contextmanagers import CONTEXT_MANAGER_EXIT_DO_NOT_SUPPRESS_EXCEPTION
from zero.mouse import MouseMotion
from zero.type_wrappers.typed_dict import PygameMouseMotionEventDict

logger = logging.getLogger(__name__)


class Game:
    def __init__(self) -> None:
        self._next_mouse_motion_subscribers: Queue[Future[MouseMotion]] = Queue()
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
        _exc_type: type[BaseException] | None,
        _exc_val: BaseException | None,
        _exc_tb: TracebackType | None,
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
                elif event.type == pygame.MOUSEMOTION:
                    await self.publish_mouse_motion_event(
                        cast(PygameMouseMotionEventDict, event.dict)
                    )

            pygame.display.flip()

            # yield event loop
            await sleep(0)
            clock.tick(self._fps)

    async def publish_mouse_motion_event(
        self, mouse_motion_event: PygameMouseMotionEventDict
    ) -> None:
        while not self._next_mouse_motion_subscribers.empty():
            f = self._next_mouse_motion_subscribers.get_nowait()
            f.set_result(MouseMotion.from_pygame(mouse_motion_event))

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

    async def wait_for_next_mouse_motion(self) -> MouseMotion:
        f: Future[MouseMotion] = Future()
        await self._notify_next_mouse_motion(f)
        return await f

    async def _notify_next_mouse_motion(self, f: Future[MouseMotion]) -> None:
        await self._next_mouse_motion_subscribers.put(f)
