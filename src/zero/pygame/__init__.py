from zero.core import Platform, Zero
from zero.core.types import DisplayResolution
import pygame


class PygamePlatform(Platform):
    def __enter__(self) -> Platform:
        pygame.init()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pygame.quit()


def main():
    with PygamePlatform() as platform:
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
