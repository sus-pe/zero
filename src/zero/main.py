from __future__ import annotations

from zero.builtins import Pixels
from zero.builtins import Resolution
from zero.core import Zero
from zero.pygame import PygamePlatform

if __name__ == "__main__":
    resolution = Resolution(
        width=Pixels(800),
        height=Pixels(600),
    )

    zero = Zero(platform=PygamePlatform())
    print(resolution, zero)
