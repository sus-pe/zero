from dataclasses import dataclass
from functools import cached_property

from zero.type_wrappers.arithmetic import NonNegInt


class WindowX(NonNegInt):
    pass


class WindowY(NonNegInt):
    pass


@dataclass(frozen=True)
class WindowXY:
    x: WindowX
    y: WindowY

    @cached_property
    def negated(self) -> "WindowXY | tuple[int, int]":
        """
        If the origin is negated, then the origin is returned.
        """
        if self.is_origin:
            return self

        return -self.x, -self.y

    @cached_property
    def is_origin(self) -> bool:
        return self.x == 0 and self.y == 0

    @classmethod
    def zero_origin(cls) -> "WindowXY":
        return WindowXY.from_xy(0, 0)

    @classmethod
    def from_xy(cls, x: int, y: int) -> "WindowXY":
        x = WindowX(x)
        y = WindowY(y)
        return cls(x, y)

    def __add__(self, other: "WindowXY") -> "WindowXY":
        return WindowXY.from_xy(self.x + other.x, self.y + other.y)

    def __len__(self) -> int:
        return 2

    def __getitem__(self, item: int) -> int:
        assert 0 <= item < len(self)
        if item == 0:
            return self.x
        return self.y

    @cached_property
    def tuple(self) -> tuple[WindowX, WindowY]:
        return (self.x, self.y)
