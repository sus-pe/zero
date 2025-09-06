from contextlib import nullcontext
from dataclasses import dataclass, replace
from functools import cached_property
from os import environ
from typing import ClassVar

import pygame
from pygame import Surface

from zero.contextmanagers import suppress_no_fast_renderer_warning
from zero.sdl import SDL_VIDEODRIVER_ENV_KEY
from zero.type_wrappers.arithmetic import NonNegInt


@dataclass(frozen=True)
class DisplayConfig:
    is_scaled: bool
    is_hidden: bool
    is_fullscreen: bool
    is_allow_no_fast_renderer: bool

    SLOW_RENDERER_ERROR_MSG: ClassVar[str] = "Dummy driver is slow with scaled."

    @cached_property
    def is_dummy_display(self) -> bool:
        return (
            environ[SDL_VIDEODRIVER_ENV_KEY] == "dummy"
            if SDL_VIDEODRIVER_ENV_KEY in environ
            else False
        )

    def __post_init__(self) -> None:
        self._assert_safe_flags()

    @cached_property
    def supported_resolutions(self) -> list[tuple[NonNegInt, NonNegInt]]:
        res = [
            (NonNegInt(x), NonNegInt(y)) for x, y in pygame.display.get_desktop_sizes()
        ]
        assert len(res) > 0, "Should be at least one supported resolution!"
        return res

    @cached_property
    def pygame_flags(self) -> int:
        flags = 0

        if self.is_fullscreen:
            flags |= pygame.FULLSCREEN

        if self.is_scaled:
            flags |= pygame.SCALED

        if self.is_hidden:
            flags |= pygame.HIDDEN

        return flags

    @cached_property
    def as_fullscreen(self) -> "DisplayConfig":
        return replace(self, is_fullscreen=True)

    @cached_property
    def is_windowed(self) -> bool:
        return not self.is_fullscreen

    @cached_property
    def as_windowed(self) -> "DisplayConfig":
        return replace(self, is_fullscreen=False)

    def _assert_safe_flags(self) -> None:
        flags = self.pygame_flags
        if flags & pygame.FULLSCREEN:
            assert not flags & pygame.RESIZABLE, (
                "Resizeable and Fullscreen are incompatible."
            )
        if flags & pygame.SCALED and not self.is_allow_no_fast_renderer:
            assert not self.is_dummy_display, self.SLOW_RENDERER_ERROR_MSG


@dataclass(frozen=True)
class Display:
    config: DisplayConfig
    caption: str = "Jesus"

    @cached_property
    def surface(
        self,
    ) -> Surface:
        context = (
            suppress_no_fast_renderer_warning()
            if self.config.is_allow_no_fast_renderer
            else nullcontext()
        )
        with context:
            surface = pygame.display.set_mode(
                self.config.supported_resolutions[0], flags=self.config.pygame_flags
            )
        pygame.display.set_caption(self.caption)
        return surface

    @cached_property
    def is_fullscreen(self) -> bool:
        return self.config.is_fullscreen

    @cached_property
    def is_windowed(self) -> bool:
        return self.config.is_windowed

    @cached_property
    def as_fullscreen(self) -> "Display":
        if self.is_fullscreen:
            return self

        return Display(self.config.as_fullscreen)

    @cached_property
    def as_windowed(self) -> "Display":
        if self.is_windowed:
            return self

        return Display(
            config=self.config.as_windowed,
            caption=self.caption,
        )

    @cached_property
    def toggled_fullscreen(self) -> "Display":
        assert self.is_fullscreen or self.is_windowed
        if self.is_windowed:
            return self.as_fullscreen
        return self.as_windowed

    FULLSCREEN_FLAG: ClassVar[int] = pygame.FULLSCREEN
    RESIZEABLE_FLAG: ClassVar[int] = pygame.RESIZABLE
    SCALED_FLAG: ClassVar[int] = pygame.SCALED
