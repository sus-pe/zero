from __future__ import annotations

import pytest
from zero.core.types import NonNegativeInt
from zero.core.types import Pixels
from zero.core.types import Resolution


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
    Resolution(width=Pixels(640), height=Pixels(640))
