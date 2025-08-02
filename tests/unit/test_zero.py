import pytest
from zero.builtins import NonNegativeInt, Pixels, Resolution


def test_positive_int():
    p = NonNegativeInt(1)
    assert p + 1 == 2
    with pytest.raises(ValueError):
        NonNegativeInt(-1)


def test_pixel():
    p = Pixels(640)
    assert p + 1 == 641
    with pytest.raises(ValueError):
        Pixels(-640)


def test_resolution():
    r = Resolution(width=640, height=480)
