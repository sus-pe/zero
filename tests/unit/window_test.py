from dataclasses import dataclass
from functools import cached_property

import numpy as np
from pytest import fixture

from zero.type_wrappers.arithmetic import WindowPixels, WindowX, WindowXY, WindowY


@dataclass(frozen=True)
class Window:
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


@fixture
def stub_pixels() -> WindowPixels:
    rows = 1920
    cols = 1080
    return np.arange(rows * cols, dtype=np.int32).reshape(rows, cols)


def test_window_xy() -> None:
    assert WindowXY.from_xy(0, 0) + WindowXY.from_xy(1, 1) == WindowXY.from_xy(1, 1)


def test_window(stub_pixels: WindowPixels) -> None:
    window = Window(stub_pixels)
    assert window.width == stub_pixels.shape[0]
    assert window.height == stub_pixels.shape[1]
    xy = WindowXY.from_xy(0, 0)
    assert window.is_containing_at(xy=xy, other=stub_pixels)
