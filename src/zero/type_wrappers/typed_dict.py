from typing import TypedDict

from zero.type_wrappers.arithmetic import (
    LeftMouseBit,
    MiddleMouseBit,
    RightMouseBit,
)


class PygameEventDict(TypedDict):
    pass


class PygameMouseMotionEventDict(PygameEventDict):
    pos: tuple[int, int]  # note: can be negative!
    rel: tuple[int, int]
    buttons: tuple[LeftMouseBit, MiddleMouseBit, RightMouseBit]
