from typing import TypedDict

from zero.type_wrappers.arithmetic import (
    LeftMouseBit,
    MiddleMouseBit,
    RightMouseBit,
)
from zero.type_wrappers.window import WindowX, WindowY


class PygameEventDict(TypedDict):
    pass


class PygameMouseMotionEventDict(PygameEventDict):
    pos: tuple[WindowX, WindowY]
    rel: tuple[int, int]
    buttons: tuple[LeftMouseBit, MiddleMouseBit, RightMouseBit]
