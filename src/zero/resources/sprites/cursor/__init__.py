from dataclasses import dataclass
from functools import cached_property
from pathlib import Path
from typing import cast

import numpy as np
import numpy.typing as npt
import pygame
from pygame import Rect, Surface

from zero.type_wrappers.arithmetic import Bit, NonNegInt
from zero.type_wrappers.window import WindowXY

CURSOR_PATH = Path(__file__).parent.joinpath("cursor.png")


@dataclass(frozen=True)
class Sprite:
    _surface: Surface

    @cached_property
    def as_np(self) -> npt.NDArray[np.int32]:
        copy = pygame.surfarray.array2d(self._surface)
        copy.flags.writeable = False
        return copy

    @cached_property
    def width(self) -> NonNegInt:
        return NonNegInt(self._surface.get_width())

    @cached_property
    def height(self) -> NonNegInt:
        return NonNegInt(self._surface.get_height())

    @cached_property
    def rect(self) -> Rect:
        return Rect(0, 0, self.width, self.height)

    @cached_property
    def surface(self) -> Surface:
        return self._surface.copy()

    @cached_property
    def size(self) -> tuple[NonNegInt, NonNegInt]:
        return (self.width, self.height)

    @cached_property
    def total_pixels(self) -> NonNegInt:
        return NonNegInt(self.width * self.height)

    def subsprite(self, rect: Rect) -> "Sprite":
        return self.from_surface(self._surface.subsurface(rect).copy())

    def is_displayed_by(self, other: "Sprite | Surface") -> bool:
        if self.size != other.size:
            return False

        return self.count_equivalent_pixels(other) == self.total_pixels

    def count_equivalent_pixels(self, other: "Sprite | Surface") -> NonNegInt:
        assert self.size == other.size, "Supposed to be same size to compare pixels!"
        if isinstance(other, Sprite):
            return self._count_equivalent_pixels(other.surface)
        return self._count_equivalent_pixels(other)

    def _count_equivalent_pixels(self, other: Surface) -> NonNegInt:
        return NonNegInt(
            pygame.transform.threshold(
                surface=self.surface,
                search_surf=other,
                dest_surface=None,
                search_color=None,
                set_behavior=Bit.zero,
            )
        )

    def rect_at(self, offset: WindowXY) -> Rect:
        return self.rect.move(offset.x, offset.y)

    def convert(self) -> "Sprite":
        return self.from_surface(self._surface.convert_alpha())

    def blit_to(self, target: Surface, xy: WindowXY) -> None:
        target.blit(self._surface, xy)

    @classmethod
    def _load_surface(cls, path: Path) -> Surface:
        assert path.is_file()
        return pygame.image.load(path)

    @classmethod
    def from_surface(cls, surface: Surface) -> "Sprite":
        return cls(surface)


@dataclass(frozen=True)
class MouseCursorSprite(Sprite):
    @classmethod
    def load(cls, path: Path = CURSOR_PATH) -> "MouseCursorSprite":
        return cls.from_surface(cls._load_surface(path))

    @classmethod
    def from_surface(cls, surface: Surface) -> "MouseCursorSprite":
        return cast(MouseCursorSprite, super().from_surface(surface))
