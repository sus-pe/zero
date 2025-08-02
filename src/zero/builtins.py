from __future__ import annotations

from dataclasses import dataclass


class NonNegativeInt(int):
    def __new__(cls, value: int):
        if value < 0:
            raise ValueError(f"Value must be non-negative: {value=}")
        return super().__new__(cls, value)


class Pixels(NonNegativeInt):
    pass


@dataclass(frozen=True)
class Resolution:
    width: Pixels
    height: Pixels
