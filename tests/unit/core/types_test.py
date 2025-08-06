from __future__ import annotations

import pytest
from pydantic import ValidationError

from zero.core.types import NonNegativeInt
from zero.core.types import Pixels
from zero.core.types import Resolution


def test_pixel():
    Pixels(value=640)
    with pytest.raises(ValidationError):
        Pixels(value=-640)


def test_resolution():
    Resolution(width=Pixels(value=640), height=Pixels(value=640))


def test_non_int_is_nonnegint():
    def f(i: NonNegativeInt):
        pass

    f(1)
