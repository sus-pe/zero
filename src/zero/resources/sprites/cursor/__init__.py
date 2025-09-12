from dataclasses import dataclass
from functools import cached_property, lru_cache
from importlib.resources import files
from importlib.resources.abc import Traversable
from io import BytesIO
from typing import cast

import pygame
from pygame import Rect, Surface

from zero.type_wrappers.arithmetic import Bit, NonNegInt
from zero.type_wrappers.window import WindowXY


@dataclass(frozen=True)
class Sprite:
    _surface: Surface

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
    def _load_surface(cls, asset: Traversable) -> Surface:
        assert asset.is_file(), f"Provided {asset=} could not be found!"
        return cls._load_surface_from_bytes(asset.read_bytes(), asset.name)

    @classmethod
    @lru_cache
    def _load_surface_from_bytes(cls, raw: bytes, name: str) -> Surface:
        return pygame.image.load(BytesIO(raw), name)

    @classmethod
    def from_surface(cls, surface: Surface) -> "Sprite":
        return cls(surface)


@dataclass(frozen=True)
class MouseCursorSprite(Sprite):
    @classmethod
    def load(cls) -> "MouseCursorSprite":
        asset = files(__package__).joinpath("cursor.png")
        return cls.from_surface(cls._load_surface(asset))

    @classmethod
    def from_surface(cls, surface: Surface) -> "MouseCursorSprite":
        return cast(MouseCursorSprite, super().from_surface(surface))


@dataclass(frozen=True)
class PressedMouseCursorSprite(Sprite):
    @classmethod
    def load(cls) -> "PressedMouseCursorSprite":
        asset = files(__package__).joinpath("pressed_cursor.png")
        return cls.from_surface(cls._load_surface(asset))

    @classmethod
    def from_surface(cls, surface: Surface) -> "PressedMouseCursorSprite":
        return cast(PressedMouseCursorSprite, super().from_surface(surface))


@dataclass(frozen=True)
class ButtonSprite(Sprite):
    @classmethod
    def load(cls) -> "ButtonSprite":
        asset = files(__package__).joinpath("button.png")
        return cls.from_surface(cls._load_surface(asset))

    @classmethod
    def from_surface(cls, surface: Surface) -> "ButtonSprite":
        return cast(ButtonSprite, super().from_surface(surface))
