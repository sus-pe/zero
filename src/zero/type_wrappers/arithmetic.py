from collections.abc import Generator
from typing import cast


class NonNegInt(int):
    def __new__(cls, value: int) -> "NonNegInt":
        if value < 0:
            raise NegIntError(value)
        return super().__new__(cls, value)


class NegIntError(ValueError):
    def __init__(self, x: int) -> None:
        super().__init__(f"Negative integer: {x}")


class Bit(NonNegInt):
    zero: "Bit"
    one: "Bit"

    def __new__(cls, value: int) -> "Bit":
        if value not in {0, 1}:
            raise NotBitError(value)
        return cast(Bit, super().__new__(cls, value))

    @classmethod
    def alternating(cls, size: int) -> Generator["Bit"]:
        for i in range(size):
            yield Bit(i % 2)


Bit.zero = Bit(0)
Bit.one = Bit(1)


class NotBitError(ValueError):
    def __init__(self, x: int) -> None:
        super().__init__(f"Not a bit: {x}")


class LeftMouseBit(Bit):
    pass


class RightMouseBit(Bit):
    pass


class MiddleMouseBit(Bit):
    pass


class Trit(NonNegInt):
    zero: "Trit"
    one: "Trit"
    two: "Trit"

    def __new__(cls, value: int) -> "Trit":
        if value not in {0, 1, 2}:
            raise NotTritError(value)
        return cast(Trit, super().__new__(cls, value))


Trit.zero = Trit(0)
Trit.one = Trit(1)
Trit.two = Trit(2)


class NotTritError(ValueError):
    def __init__(self, x: int) -> None:
        super().__init__(f"Not a bit: {x}")
