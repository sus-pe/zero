from dataclasses import dataclass
from functools import cached_property

from zero.pygame_event_factory import (
    PygameEventFactory,
    PygameMouseMotionEvent,
)
from zero.type_wrappers.arithmetic import (
    Bit,
    LeftMouseBit,
    MiddleMouseBit,
    RightMouseBit,
)
from zero.type_wrappers.typed_dict import PygameMouseMotionEventDict
from zero.type_wrappers.window import WindowX, WindowXY, WindowY


@dataclass(frozen=True)
class MouseCursorEvent:
    xy: WindowXY
    dx: int
    dy: int
    left: LeftMouseBit
    middle: MiddleMouseBit
    right: RightMouseBit

    @cached_property
    def x(self) -> WindowX:
        return self.xy.x

    @cached_property
    def y(self) -> WindowY:
        return self.xy.y

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
    ) -> "MouseCursorEvent":
        return cls(
            xy=WindowXY.from_xy(x=x, y=y),
            dx=dx,
            dy=dy,
            left=LeftMouseBit(left),
            middle=MiddleMouseBit(middle),
            right=RightMouseBit(right),
        )

    @classmethod
    def from_pygame(cls, d: PygameMouseMotionEventDict) -> "MouseCursorEvent":
        return cls(
            xy=WindowXY.from_xy(x=d["pos"][0], y=d["pos"][1]),
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


class Mouse:
    def __init__(self) -> None:
        self.cursor_xy = WindowXY.zero_origin()
        self.left: Bit = Bit.zero
        self.middle: Bit = Bit.zero
        self.right: Bit = Bit.zero

    def update(self, event: MouseCursorEvent) -> None:
        self.cursor_xy = event.xy
        self.left = event.left
        self.middle = event.middle
        self.right = event.right
