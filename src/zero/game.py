import logging
from asyncio import Event, Future, Queue, Task, create_task, sleep
from contextlib import suppress
from functools import cached_property
from typing import cast

import pygame
from pygame import Clock, Surface

from zero.mouse import Mouse, MouseCursorEvent
from zero.resources.loader import ResourceLoader
from zero.resources.sprites.cursor import (
    MouseCursorSprite,
    PressedMouseCursorSprite,
    Sprite,
)
from zero.type_wrappers.arithmetic import NonNegInt
from zero.type_wrappers.typed_dict import PygameMouseMotionEventDict
from zero.type_wrappers.window import WindowXY

logger = logging.getLogger(__name__)

CursorController = Task[None]


class Game:
    def __init__(self, resource_loader: ResourceLoader) -> None:
        self._resource_loader = resource_loader
        self._window_surface: Surface | None = None
        self._mouse: Mouse | None = None
        self._next_mouse_motion_subscribers: Queue[
            Future[MouseCursorEvent] | Queue[MouseCursorEvent]
        ] = Queue()
        self._window_task: Task[None] | None = None
        self._fps: NonNegInt = NonNegInt(240)
        self._resolution = (NonNegInt(1280), NonNegInt(720))
        self._cursor_controller: CursorController | None = None
        self._loop_event: Event = Event()
        self._is_loop_finished_event: Event = Event()
        self._is_loop_started_event: Event = Event()

    async def wait_exit(self) -> None:
        await self._is_loop_finished_event.wait()

    async def setup_display(self, flags: int) -> None:
        assert not self._window_surface, "Not supposed to be initialized yet!"
        self._window_surface = pygame.display.set_mode(self._resolution, flags)
        pygame.display.set_caption("Automated Test Window")
        self._fill_window_with_black()

    async def game_loop_until_quit(self) -> None:
        assert self._fps > 0
        assert self._window_surface, "Supposed to be initialized!"
        assert self._mouse, "Supposed to be initialized!"
        assert not self._is_loop_finished_event.is_set()
        assert not self._is_loop_started_event.is_set()

        self._is_loop_started_event.set()
        running = True
        clock: Clock = pygame.time.Clock()
        try:
            while running:
                is_quit = await self._do_one_loop()
                running = not is_quit
                # yield event loop
                await sleep(0)
                self._loop_event.set()
                clock.tick(self._fps)
                self._loop_event.clear()
        finally:
            assert self._is_loop_started_event.is_set()
            assert not self._is_loop_finished_event.is_set()
            self._is_loop_finished_event.set()

    async def _do_one_loop(self) -> bool:
        is_quit: bool = False
        self._fill_window_with_black()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_quit = True
            elif event.type == pygame.MOUSEMOTION:
                await self.publish_mouse_motion_event(
                    cast(PygameMouseMotionEventDict, event.dict)
                )
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_F11:
                # TODO: PUBSUB!
                self.toggle_fullscreen()
        self._render_mouse_cursor()
        pygame.display.flip()
        return is_quit

    async def wait_loop_started(self) -> None:
        await self._is_loop_started_event.wait()

    async def wait_next_loop(self) -> None:
        assert self._is_loop_started_event.is_set()
        assert not self._is_loop_finished_event.is_set()
        await self._loop_event.wait()

    async def publish_mouse_motion_event(
        self, mouse_motion_event: PygameMouseMotionEventDict
    ) -> None:
        mouse_motion = MouseCursorEvent.from_pygame(mouse_motion_event)
        requeue_subs: list[Queue[MouseCursorEvent]] = []
        while not self._next_mouse_motion_subscribers.empty():
            sub = self._next_mouse_motion_subscribers.get_nowait()
            if isinstance(sub, Future):
                sub.set_result(mouse_motion)
            elif isinstance(sub, Queue):
                await sub.put(mouse_motion)
                requeue_subs.append(sub)

        for sub in requeue_subs:
            await self._next_mouse_motion_subscribers.put(sub)

    async def send_quit(self) -> None:
        pygame.event.post(pygame.event.Event(pygame.QUIT))

    async def try_send_quit(self) -> None:
        with suppress(pygame.error):
            await self.send_quit()

    async def wait_for_next_mouse_motion(self) -> MouseCursorEvent:
        f: Future[MouseCursorEvent] = Future()
        await self._notify_next_mouse_motion(f)
        return await f

    async def _notify_next_mouse_motion(self, f: Future[MouseCursorEvent]) -> None:
        await self._next_mouse_motion_subscribers.put(f)

    def send_mouse_motion(self, expected_mouse: MouseCursorEvent) -> None:
        pygame.event.post(expected_mouse.as_pygame_event())

    def get_mouse_cursor_xy(self) -> WindowXY:
        assert self._mouse, "Supposed to be initialized"
        return self._mouse.cursor_xy

    async def setup_mouse_cursor(self) -> None:
        assert not self._mouse, "Not supposed to be initiazlied yet."
        assert self.is_os_cursor_visible()
        self.hide_os_cursor()
        assert self.is_os_cursor_hidden()
        cursor_events_queue = await self._start_cursor_controller()
        self._mouse = Mouse()
        await self._next_mouse_motion_subscribers.put(cursor_events_queue)

    async def _start_cursor_controller(self) -> Queue[MouseCursorEvent]:
        event_queue: Queue[MouseCursorEvent] = Queue()
        self._cursor_controller = create_task(
            self._cursor_controller_coroutine(event_queue)
        )
        return event_queue

    async def _cursor_controller_coroutine(
        self, events: Queue[MouseCursorEvent]
    ) -> None:
        while not self._is_loop_finished_event.is_set():
            event = await events.get()
            assert self._mouse, "Supposed to be initialized!"
            self._mouse.update(event)

    @cached_property
    def mouse_cursor_sprite(self) -> MouseCursorSprite:
        assert self._window_surface, "Supposed to be initialized!"
        return self._resource_loader.convert_cursor_sprite

    @cached_property
    def mouse_cursor_pressed_sprite(self) -> PressedMouseCursorSprite:
        assert self._window_surface, "Supposed to be initialized!"
        return self._resource_loader.convert_pressed_cursor_sprite

    def _render_mouse_cursor(self) -> None:
        assert self._window_surface, "Supposed to be initialized!"
        assert self._mouse, "Supposed to be initialized!"
        if self._mouse.left:
            sprite: Sprite = self.mouse_cursor_pressed_sprite
        else:
            sprite = self.mouse_cursor_sprite

        sprite.blit_to(self._window_surface, self._mouse.cursor_xy)

    def is_displayed(self, sprite: Sprite, xy: WindowXY) -> bool:
        assert self._window_surface, "Supposed to be initialized!"
        display_rect = self._window_surface.subsurface(sprite.rect_at(xy))
        return sprite.is_displayed_by(display_rect)

    def is_os_cursor_visible(self) -> bool:
        return pygame.mouse.get_visible()

    def is_os_cursor_hidden(self) -> bool:
        return not self.is_os_cursor_visible()

    def hide_os_cursor(self) -> None:
        pygame.mouse.set_visible(False)

    def is_fullscreen(self) -> bool:
        assert self._window_surface, "Supposed to be initialized!"
        return bool(self._window_surface.get_flags() & pygame.FULLSCREEN)

    def is_windowed(self) -> bool:
        return not self.is_fullscreen()

    def set_fullscreen(self) -> None:
        assert self._window_surface, "Supposed to be initialized!"
        if not self.is_fullscreen():
            new_flags = self._window_surface.get_flags() | pygame.FULLSCREEN
            self._window_surface = pygame.display.set_mode(self._resolution, new_flags)

    def set_windowed(self) -> None:
        assert self._window_surface, "Supposed to be initialized!"
        if not self.is_windowed():
            flags = self._window_surface.get_flags()
            new_flags = flags & ~pygame.FULLSCREEN
            self._window_surface = pygame.display.set_mode(self._resolution, new_flags)

    def send_f11(self) -> None:
        pygame.event.post(pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_F11}))

    def toggle_fullscreen(self) -> None:
        if self.is_fullscreen():
            self.set_windowed()
        else:
            self.set_fullscreen()

    def _fill_window_with_black(self) -> None:
        assert self._window_surface, "Supposed to be initialized!"
        self._window_surface.fill((0, 0, 0))
