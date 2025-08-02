from __future__ import annotations

from zero.builtins import Pixels
from zero.builtins import Resolution

if __name__ == "__main__":
    resolution = Resolution(
        width=Pixels(800),
        height=Pixels(600),
    )
    print(resolution)
