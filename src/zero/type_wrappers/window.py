from dataclasses import dataclass
from functools import cached_property

import numpy as np
from numpy import typing as npt

from zero.type_wrappers.arithmetic import NonNegInt


class WindowX(NonNegInt):
    pass


class WindowY(NonNegInt):
    pass


@dataclass(frozen=True)
class WindowXY:
    x: WindowX
    y: WindowY

    @classmethod
    def from_xy(cls, x: int, y: int) -> "WindowXY":
        x = WindowX(x)
        y = WindowY(y)
        return cls(x, y)

    def __add__(self, other: "WindowXY") -> "WindowXY":
        return WindowXY.from_xy(self.x + other.x, self.y + other.y)

    def __ge__(self, other: "WindowXY") -> bool:
        return self.x >= other.x and self.y >= other.y

    def __len__(self) -> int:
        return 2

    def __getitem__(self, item: int) -> int:
        assert 0 <= item < len(self)
        if item == 0:
            return self.x
        return self.y


WindowPixels = npt.NDArray[np.int32]


@dataclass(frozen=True)
class WindowView:
    pixels: WindowPixels

    @cached_property
    def width(self) -> WindowX:
        return self.pixels.shape[0]

    @cached_property
    def height(self) -> WindowY:
        return self.pixels.shape[1]

    def is_containing_at(self, xy: WindowXY, other: WindowPixels) -> bool:
        required_minimum_shape = xy + WindowXY.from_xy(*other.shape)
        return required_minimum_shape >= WindowXY.from_xy(*self.pixels.shape)

    def contains(self, pixels: WindowPixels, *, at: WindowXY) -> bool:
        spare_width = self.width - at.x
        width = pixels.shape[0]
        if width > spare_width:
            return False

        spare_height = self.height - at.y
        height = pixels.shape[1]
        if height > spare_height:
            return False

        window_slice = self.pixels[at.x : at.x + width, at.y : at.y + height]
        return np.array_equal(window_slice, pixels)
