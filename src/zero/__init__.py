from zero.core.types import Pixels
from zero.core.types import Resolution
from zero.core import Zero
from zero.pygame import PygamePlatform


def main():
    resolution = Resolution(
        width=Pixels(800),
        height=Pixels(600),
    )
    zero = Zero(platform=PygamePlatform())
    print(resolution, zero)


if __name__ == "__main__":  # pragma: no cover
    main()
