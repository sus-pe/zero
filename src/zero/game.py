import logging
from asyncio import Event as AsyncEvent
from asyncio import Future, Queue, Task, TaskGroup, sleep
from contextlib import suppress
from functools import cached_property
from typing import cast

import pygame
from pygame import Clock
from pygame import Event as PygameEvent

from zero.display import Display
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


class ExitEvent:
    pass


type Event[T] = T | ExitEvent
type FutureEvent[T] = Future[Event[T]]
type EventQueue[T] = Queue[Event[T]]
type EventSubscriber[T] = EventQueue[T] | FutureEvent[T]
type EventSubscribers[T] = Queue[EventSubscriber[T]]


class Game:
    EXIT_EVENT = ExitEvent()

    def __init__(
        self,
        resource_loader: ResourceLoader,
        fps: NonNegInt,
        display: Display,
        task_group: TaskGroup,
    ) -> None:
        self._task_group = task_group
        self._resource_loader = resource_loader
        self._display = display
        self._mouse: Mouse | None = None
        self._next_mouse_motion_subscribers: EventSubscribers[MouseCursorEvent] = (
            Queue()
        )
        self._fps = fps
        self._cursor_controller: CursorController | None = None
        self._loop_event: AsyncEvent = AsyncEvent()
        self._is_loop_finished_event: AsyncEvent = AsyncEvent()
        self._is_loop_started_event: AsyncEvent = AsyncEvent()

    @property
    def display(self) -> Display:
        return self._display

    async def wait_exit(self) -> None:
        await self._is_loop_finished_event.wait()

    async def game_loop_until_quit(self) -> None:
        assert self._fps > 0
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
            self._loop_event.set()  # Ensure no waiters.
            assert self._is_loop_started_event.is_set()
            assert not self._is_loop_finished_event.is_set()
            self._is_loop_finished_event.set()
            await self.publish_exit_event()

    async def publish_exit_event(self) -> None:
        await self.publish_to(self._next_mouse_motion_subscribers, self.EXIT_EVENT)

    async def _do_one_loop(self) -> bool:
        is_quit: bool = False
        self.display.surface.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_quit = True
            elif event.type == pygame.MOUSEMOTION:
                await self.publish_mouse_motion_event(
                    cast(PygameMouseMotionEventDict, event.dict)
                )
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_F11:
                self._display = self._display.toggled_fullscreen
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
        mouse_motion_event["pos"] = self.display.clamp(mouse_motion_event["pos"]).tuple
        mouse_motion = MouseCursorEvent.from_pygame(mouse_motion_event)
        await self.publish_to(self._next_mouse_motion_subscribers, mouse_motion)

    async def publish_to[T](
        self, subscribers: EventSubscribers[T], event: Event[T]
    ) -> None:
        requeue_subs: list[EventQueue[T]] = []
        while not subscribers.empty():
            sub = subscribers.get_nowait()
            if isinstance(sub, Future):
                sub.set_result(event)
            elif isinstance(sub, Queue):
                await sub.put(event)
                requeue_subs.append(sub)

        for sub in requeue_subs:
            await subscribers.put(sub)

    def send_quit(self) -> None:
        pygame.event.post(pygame.event.Event(pygame.QUIT))

    async def try_send_quit(self) -> None:
        with suppress(pygame.error):
            self.send_quit()

    async def wait_for_next_mouse_motion(self) -> Event[MouseCursorEvent]:
        f: FutureEvent[MouseCursorEvent] = Future()
        await self._notify_next_mouse_motion(f)
        return await f

    async def _notify_next_mouse_motion(
        self, f: EventSubscriber[MouseCursorEvent]
    ) -> None:
        await self._next_mouse_motion_subscribers.put(f)

    def send_mouse_motion(self, expected_mouse: MouseCursorEvent) -> None:
        pygame.event.post(expected_mouse.as_pygame_event())

    def get_mouse_cursor_xy(self) -> WindowXY:
        assert self._mouse, "Supposed to be initialized"
        return self._mouse.cursor_xy

    async def setup_mouse_cursor(self) -> None:
        assert not self._mouse, "Not supposed to be initiazlied yet."
        self.hide_os_cursor()
        assert self.is_os_cursor_hidden()
        cursor_events_queue = await self._start_cursor_controller()
        self._mouse = Mouse()
        await self._next_mouse_motion_subscribers.put(cursor_events_queue)

    async def _start_cursor_controller(self) -> EventQueue[MouseCursorEvent]:
        event_queue: EventQueue[MouseCursorEvent] = Queue()
        self._cursor_controller = self._task_group.create_task(
            self._cursor_controller_coroutine(event_queue)
        )
        return event_queue

    async def _cursor_controller_coroutine(
        self, events: EventQueue[MouseCursorEvent]
    ) -> None:
        while not self._is_loop_finished_event.is_set():
            event = await events.get()
            if event == self.EXIT_EVENT:
                break

            assert self._mouse, "Supposed to be initialized!"
            assert isinstance(event, MouseCursorEvent)
            self._mouse.update(event)

    @cached_property
    def mouse_cursor_sprite(self) -> MouseCursorSprite:
        return self._resource_loader.convert_cursor_sprite

    @cached_property
    def mouse_cursor_pressed_sprite(self) -> PressedMouseCursorSprite:
        return self._resource_loader.convert_pressed_cursor_sprite

    def _render_mouse_cursor(self) -> None:
        assert self._mouse, "Supposed to be initialized!"
        if self._mouse.left:
            sprite: Sprite = self.mouse_cursor_pressed_sprite
        else:
            sprite = self.mouse_cursor_sprite

        sprite.blit_to(self.display.surface, self._mouse.cursor_xy)

    def is_displayed(self, sprite: Sprite, xy: WindowXY) -> bool:
        display_rect = self.display.surface.subsurface(sprite.rect_at(xy))
        return sprite.is_displayed_by(display_rect)

    def is_os_cursor_visible(self) -> bool:
        return pygame.mouse.get_visible()

    def is_os_cursor_hidden(self) -> bool:
        return not self.is_os_cursor_visible()

    def hide_os_cursor(self) -> None:
        pygame.mouse.set_visible(False)

    def send_f11(self) -> None:
        pygame.event.post(pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_F11}))

    def send(self, event: PygameEvent) -> None:
        pygame.event.post(event)
