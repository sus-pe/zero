from dataclasses import dataclass
from typing import TypeAlias

PositiveInt: TypeAlias = int


class Pixels:
    def __init__(self, value: PositiveInt):
        assert value > 0
        self._value = value


@dataclass(frozen=True)
class Resolution:
    width: Pixels
    height: Pixels
