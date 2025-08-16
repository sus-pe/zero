from dataclasses import dataclass

from zero.pygame_event_factory import (
    PygameEventFactory,
    PygameMouseMotionEvent,
)
from zero.type_wrappers.arithmetic import (
    LeftMouseBit,
    MiddleMouseBit,
    RightMouseBit,
    WindowX,
    WindowY,
)
from zero.type_wrappers.typed_dict import PygameMouseMotionEventDict


@dataclass(frozen=True)
class MouseMotion:
    x: WindowX
    y: WindowY
    dx: int
    dy: int
    left: LeftMouseBit
    middle: MiddleMouseBit
    right: RightMouseBit

    @classmethod
    def from_xy(
        cls,
        x: int,
        y: int,
        dx: int = 0,
        dy: int = 0,
        left: int = 0,
        middle: int = 0,
        right: int = 0,
    ) -> "MouseMotion":
        return cls(
            x=WindowX(x),
            y=WindowY(y),
            dx=dx,
            dy=dy,
            left=LeftMouseBit(left),
            middle=MiddleMouseBit(middle),
            right=RightMouseBit(right),
        )

    @classmethod
    def from_pygame(cls, d: PygameMouseMotionEventDict) -> "MouseMotion":
        return cls(
            x=WindowX(d["pos"][0]),
            y=WindowY(d["pos"][1]),
            dx=d["rel"][0],
            dy=d["rel"][1],
            left=LeftMouseBit(d["buttons"][0]),
            middle=MiddleMouseBit(d["buttons"][1]),
            right=RightMouseBit(d["buttons"][2]),
        )

    def as_pygame(self) -> PygameMouseMotionEventDict:
        return PygameMouseMotionEventDict(
            pos=(self.x, self.y),
            rel=(self.dx, self.dy),
            buttons=(self.left, self.middle, self.right),
        )

    def as_pygame_event(self) -> PygameMouseMotionEvent:
        return PygameEventFactory.mouse_motion(
            self.as_pygame(),
        )
