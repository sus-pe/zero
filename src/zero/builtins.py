from dataclasses import dataclass


class NonNegativeInt(int):
    def __new__(cls, value: int):
        if value < 0:
            raise ValueError("Value must be non-negative")
        return super().__new__(cls, value)


class Pixels(NonNegativeInt):
    pass


@dataclass(frozen=True)
class Resolution:
    width: Pixels
    height: Pixels
