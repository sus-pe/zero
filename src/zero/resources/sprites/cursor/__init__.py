from dataclasses import dataclass
from functools import cached_property
from pathlib import Path
from typing import cast

import numpy as np
import numpy.typing as npt
import pygame
from pygame import Surface

from zero.type_wrappers.arithmetic import NonNegInt
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

    def blit_to(self, target: Surface, xy: WindowXY) -> None:
        target.blit(self._surface, xy)

    @cached_property
    def width(self) -> NonNegInt:
        return NonNegInt(self._surface.get_width())

    @cached_property
    def height(self) -> NonNegInt:
        return NonNegInt(self._surface.get_height())

    @classmethod
    def load(cls, path: Path) -> "Sprite":
        assert path.is_file()
        surface = pygame.image.load(path)
        return cls(surface)


@dataclass(frozen=True)
class MouseCursorSprite(Sprite):
    @classmethod
    def load(cls, path: Path = CURSOR_PATH) -> "MouseCursorSprite":
        return cast(MouseCursorSprite, super().load(path))
