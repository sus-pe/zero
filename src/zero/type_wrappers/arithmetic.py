class Bit(int):
    zero: "Bit"
    one: "Bit"

    def __new__(cls, value: int) -> "Bit":
        if value not in {0, 1}:
            raise NotBitError(value)
        return super().__new__(cls, value)


Bit.zero = Bit(0)
Bit.one = Bit(1)


class NotBitError(ValueError):
    def __init__(self, x: int) -> None:
        super().__init__(f"Not a bit: {x}")


class NonNegInt(int):
    def __new__(cls, value: int) -> "NonNegInt":
        if value < 0:
            raise NegIntError(value)
        return super().__new__(cls, value)


class NegIntError(ValueError):
    def __init__(self, x: int) -> None:
        super().__init__(f"Negative integer: {x}")


class LeftMouseBit(Bit):
    pass


class RightMouseBit(Bit):
    pass


class MiddleMouseBit(Bit):
    pass
