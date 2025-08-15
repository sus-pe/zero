from pytest import raises

from zero.types import Bit, NegIntError, NonNegInt, NotBitError


def test_types_non_neg() -> None:
    NonNegInt(1)
    NonNegInt(0)
    with raises(NegIntError):
        NonNegInt(-1)


def test_types_bit() -> None:
    Bit(0)
    Bit(1)
    with raises(NotBitError):
        Bit(2)
    with raises(NotBitError):
        Bit(-1)
