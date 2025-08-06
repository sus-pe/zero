from zero.core.types import DisplayResolution
from zero.core import Zero
from zero.pygame import PygamePlatform


def main():
    platform = PygamePlatform()
    zero = Zero(platform=platform)
    zero.loop_for(3)
    platform.queue_exit_command()
    zero.loop_until_exit_command()

    print(DisplayResolution.SD_4_3)
    print(DisplayResolution.FHD_1080P)
    print(DisplayResolution.HD_720P)
    print(DisplayResolution.QHD_1440P)
    print(DisplayResolution.UHD_4K)
    print(DisplayResolution.UWQHD_21_9)


if __name__ == "__main__":  # pragma: no cover
    main()
