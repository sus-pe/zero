from zero.core.types import Pixels, Loops
from zero.core.types import Resolution
from zero.core import Zero
from zero.pygame import PygamePlatform


def main():
    resolution = Resolution(
        width=Pixels(value=800),
        height=Pixels(value=600),
    )
    platform = PygamePlatform()
    zero = Zero(platform=platform)
    zero.loop_for(Loops(value=3))
    platform.queue_exit_command()
    zero.loop_until_exit_command()
    print(resolution)


if __name__ == "__main__":  # pragma: no cover
    main()
