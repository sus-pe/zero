from __future__ import annotations

from zero import Zero
from zero.core import Platform


def test_zero():
    class DummyPlatform(Platform):
        pass

    Zero(platform=DummyPlatform())
