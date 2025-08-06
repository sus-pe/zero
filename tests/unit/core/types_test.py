from __future__ import annotations

import pytest

from zero.core.types import Pixels
from zero.core.types import Resolution


def test_pixel():
    Pixels(640)
    with pytest.raises(AssertionError):
        Pixels(-640)


def test_resolution():
    Resolution(width=Pixels(value=640), height=Pixels(value=640))
