import logging
from asyncio import Event, Future, Queue, Task, create_task, sleep
from types import TracebackType
from typing import cast

import pygame
from pygame import Clock, Surface

from zero.contextmanagers import CONTEXT_MANAGER_EXIT_DO_NOT_SUPPRESS_EXCEPTION
from zero.mouse import MouseCursor, MouseCursorMotion
from zero.type_wrappers.arithmetic import WindowPixels
from zero.type_wrappers.typed_dict import PygameMouseMotionEventDict

logger = logging.getLogger(__name__)

CursorController = Task[None]


class Game:
    def __init__(self) -> None:
        self._window: Surface | None = None
        self._mouse_cursor: MouseCursor | None = None
        self._next_mouse_motion_subscribers: Queue[
            Future[MouseCursorMotion] | Queue[MouseCursorMotion]
        ] = Queue()
        self._is_quit_event: Event = Event()
        self._window_task: Task[None] | None = None
        self._is_started_event: Event = Event()
        self._fps: int = 240
        self._cursor_controller: CursorController | None = None

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
        assert not self._is_quit_event.is_set()
        assert self._window_task is not None
        await self.send_quit()
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
        mouse_motion = MouseCursorMotion.from_pygame(mouse_motion_event)
        requeue_subs: list[Queue[MouseCursorMotion]] = []
        while not self._next_mouse_motion_subscribers.empty():
            sub = self._next_mouse_motion_subscribers.get_nowait()
            if isinstance(sub, Future):
                sub.set_result(mouse_motion)
            elif isinstance(sub, Queue):
                await sub.put(mouse_motion)
                requeue_subs.append(sub)

        for sub in requeue_subs:
            await self._next_mouse_motion_subscribers.put(sub)

    async def start_game(self) -> None:
        assert not self._is_quit_event.is_set()
        assert not self._is_started_event.is_set()
        pygame.init()
        try:
            await self.setup_display()
            self.assert_resizeable()
            await self.setup_mouse_cursor()
            await self.game_loop_until_quit()
        finally:
            pygame.quit()
            assert not self._is_quit_event.is_set()
            self._is_quit_event.set()

    async def send_quit(self) -> None:
        pygame.event.post(pygame.event.Event(pygame.QUIT))

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

    async def wait_for_next_mouse_motion(self) -> MouseCursorMotion:
        f: Future[MouseCursorMotion] = Future()
        await self._notify_next_mouse_motion(f)
        return await f

    async def _notify_next_mouse_motion(self, f: Future[MouseCursorMotion]) -> None:
        await self._next_mouse_motion_subscribers.put(f)

    def send_mouse_motion(self, expected_mouse: MouseCursorMotion) -> None:
        pygame.event.post(expected_mouse.as_pygame_event())

    def get_mouse_cursor(self) -> MouseCursor:
        assert self._mouse_cursor, "Supposed to be initialized"
        return self._mouse_cursor

    async def setup_mouse_cursor(self) -> None:
        assert not self._mouse_cursor, "Not supposed to be initiazlied yet."
        cursor_events_queue = await self._start_cursor_controller()
        await self._next_mouse_motion_subscribers.put(cursor_events_queue)
        await self._load_cursor_img()

    async def _start_cursor_controller(self) -> Queue[MouseCursorMotion]:
        event_queue: Queue[MouseCursorMotion] = Queue()
        self._cursor_controller = create_task(
            self._cursor_controller_coroutine(event_queue)
        )
        return event_queue

    async def _cursor_controller_coroutine(
        self, events: Queue[MouseCursorMotion]
    ) -> None:
        while not self._is_quit_event.is_set():
            motion = await events.get()
            self._mouse_cursor = motion.cursor

    async def _load_cursor_img(self) -> None:
        pass

    def get_window_pixels(self) -> WindowPixels:
        assert self._window, "Supposed to be initialized!"
        # Soon: return pygame.surfarray.array2d(self._window)
