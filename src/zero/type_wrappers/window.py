from dataclasses import dataclass

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
