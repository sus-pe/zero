from dataclasses import dataclass
from typing import TypedDict

from zero.types import (
    Bit,
    LeftMouseBit,
    MiddleMouseBit,
    RightMouseBit,
    WindowX,
    WindowY,
)


class PygameMouseMotion(TypedDict):
    pos: tuple[WindowX, WindowY]
    rel: tuple[int, int]
    buttons: tuple[LeftMouseBit, MiddleMouseBit, RightMouseBit]


@dataclass(frozen=True)
class MouseMotion:
    x: WindowX
    y: WindowY
    dx: int = 0
    dy: int = 0
    left: Bit = Bit.zero
    middle: Bit = Bit.zero
    right: Bit = Bit.zero

    def as_pygame(self) -> PygameMouseMotion:
        return PygameMouseMotion(
            pos=(self.x, self.y),
            rel=(self.dx, self.dy),
            buttons=(self.left, self.middle, self.right),
        )

    @classmethod
    def parse(cls, x: int, y: int) -> "MouseMotion":
        return cls(x=WindowX(x), y=WindowY(y))
