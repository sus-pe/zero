import logging
from asyncio import Event, Future, Queue, Task, create_task, sleep
from contextlib import suppress
from functools import cached_property
from types import TracebackType
from typing import cast

import pygame
from pygame import Clock, Surface

from zero.contextmanagers import CONTEXT_MANAGER_EXIT_DO_NOT_SUPPRESS_EXCEPTION
from zero.mouse import MouseCursorMotion, MouseCursorXY
from zero.resources.loader import ResourceLoader
from zero.resources.sprites.cursor import MouseCursorSprite, Sprite
from zero.type_wrappers.typed_dict import PygameMouseMotionEventDict
from zero.type_wrappers.window import WindowXY

logger = logging.getLogger(__name__)

CursorController = Task[None]


class Game:
    def __init__(self) -> None:
        self._resource_fetcher = ResourceLoader()
        self._window_surface: Surface | None = None
        self._mouse_cursor: MouseCursorXY | None = None
        self._next_mouse_motion_subscribers: Queue[
            Future[MouseCursorMotion] | Queue[MouseCursorMotion]
        ] = Queue()
        self._is_started_event: Event = Event()
        self._is_quit_event: Event = Event()
        self._is_aexit_event: Event = Event()
        self._window_task: Task[None] | None = None
        self._fps: int = 240
        self._cursor_controller: CursorController | None = None

    async def __aenter__(self) -> "Game":
        assert not self._is_started_event.is_set()
        assert not self._is_quit_event.is_set()
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
        await self.try_send_quit()
        await self.wait_exit()
        assert self._is_quit_event.is_set()
        assert self._window_task, "Supposed to be initialized"
        await self._window_task
        return CONTEXT_MANAGER_EXIT_DO_NOT_SUPPRESS_EXCEPTION

    async def wait_exit(self) -> None:
        await self._is_quit_event.wait()

    async def setup_display(self) -> None:
        assert not self._window_surface, "Not supposed to be initialized yet!"
        self._window_surface = pygame.display.set_mode((640, 480), pygame.RESIZABLE)
        pygame.display.set_caption("Automated Test Window")

    async def game_loop_until_quit(self) -> None:
        assert self._fps > 0
        assert self._window_surface, "Supposed to be initialized!"
        assert self._mouse_cursor, "Supposed to be initialized!"

        running = True
        clock: Clock = pygame.time.Clock()
        while running:
            self._window_surface.fill((0, 0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEMOTION:
                    await self.publish_mouse_motion_event(
                        cast(PygameMouseMotionEventDict, event.dict)
                    )

            self._render_mouse_cursor_at(self._mouse_cursor)
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

        self._is_started_event.set()
        try:
            pygame.init()
            await self.setup_display()
            self.assert_resizeable()
            await self.setup_mouse_cursor()
            await self.game_loop_until_quit()
        finally:
            self._is_quit_event.set()
            pygame.quit()

    async def send_quit(self) -> None:
        pygame.event.post(pygame.event.Event(pygame.QUIT))

    async def try_send_quit(self) -> None:
        with suppress(pygame.error):
            await self.send_quit()

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

    def get_mouse_cursor_xy(self) -> MouseCursorXY:
        assert self._mouse_cursor, "Supposed to be initialized"
        return self._mouse_cursor

    async def setup_mouse_cursor(self) -> None:
        assert not self._mouse_cursor, "Not supposed to be initiazlied yet."
        cursor_events_queue = await self._start_cursor_controller()
        self._mouse_cursor = MouseCursorXY.zero_origin()
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
            self._render_mouse_cursor_at(self._mouse_cursor)

    async def _load_cursor_img(self) -> None:
        pass

    @cached_property
    def mouse_cursor_sprite(self) -> MouseCursorSprite:
        assert self._window_surface, "Supposed to be initialized!"
        return self._resource_fetcher.convert_cursor_sprite

    def _render_mouse_cursor_at(self, mouse_cursor: MouseCursorXY) -> None:
        assert self._window_surface, "Supposed to be initialized!"
        assert mouse_cursor, "Supposed to be initialized!"
        self.mouse_cursor_sprite.blit_to(self._window_surface, mouse_cursor)

    def is_displayed(self, sprite: Sprite, xy: WindowXY) -> bool:
        assert self._window_surface, "Supposed to be initialized!"
        display_rect = self._window_surface.subsurface(sprite.rect_at(xy))
        return sprite.is_displayed_by(display_rect)
