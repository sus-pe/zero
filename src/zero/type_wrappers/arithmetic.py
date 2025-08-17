from dataclasses import dataclass

import numpy as np
import numpy.typing as npt


class Bit(int):
    zero: "Bit"
    one: "Bit"

    def __new__(cls, value: int) -> "Bit":
        if value not in {0, 1}:
            raise NotBitError(value)
        return super().__new__(cls, value)


Bit.zero = Bit(0)
Bit.one = Bit(1)


class NotBitError(ValueError):
    def __init__(self, x: int) -> None:
        super().__init__(f"Not a bit: {x}")


class NonNegInt(int):
    def __new__(cls, value: int) -> "NonNegInt":
        if value < 0:
            raise NegIntError(value)
        return super().__new__(cls, value)


class NegIntError(ValueError):
    def __init__(self, x: int) -> None:
        super().__init__(f"Negative integer: {x}")


class LeftMouseBit(Bit):
    pass


class RightMouseBit(Bit):
    pass


class MiddleMouseBit(Bit):
    pass


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


WindowPixels = npt.NDArray[np.int32]
