from dataclasses import dataclass
from functools import cached_property

from zero.pygame_event_factory import (
    PygameEventFactory,
    PygameMouseMotionEvent,
)
from zero.type_wrappers.arithmetic import (
    LeftMouseBit,
    MiddleMouseBit,
    RightMouseBit,
    WindowX,
    WindowXY,
    WindowY,
)
from zero.type_wrappers.typed_dict import PygameMouseMotionEventDict


@dataclass(frozen=True)
class MouseCursor:
    x: WindowX
    y: WindowY

    @cached_property
    def xy(self) -> WindowXY:
        return WindowXY(self.x, self.y)

    @classmethod
    def from_xy(cls, x: int, y: int) -> "MouseCursor":
        return cls(x=WindowX(x), y=WindowY(y))


@dataclass(frozen=True)
class MouseCursorMotion:
    cursor: MouseCursor
    dx: int
    dy: int
    left: LeftMouseBit
    middle: MiddleMouseBit
    right: RightMouseBit

    @cached_property
    def x(self) -> WindowX:
        return self.cursor.x

    @cached_property
    def y(self) -> WindowY:
        return self.cursor.y

    @cached_property
    def xy(self) -> WindowXY:
        return self.cursor.xy

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
    ) -> "MouseCursorMotion":
        return cls(
            cursor=MouseCursor.from_xy(x=x, y=y),
            dx=dx,
            dy=dy,
            left=LeftMouseBit(left),
            middle=MiddleMouseBit(middle),
            right=RightMouseBit(right),
        )

    @classmethod
    def from_pygame(cls, d: PygameMouseMotionEventDict) -> "MouseCursorMotion":
        return cls(
            cursor=MouseCursor.from_xy(x=d["pos"][0], y=d["pos"][1]),
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
