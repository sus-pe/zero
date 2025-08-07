from types import TracebackType
from typing import Optional, Type

import pygame

from zero.core import Platform, Zero
from zero.core.types import DisplayResolution


class PygamePlatform(Platform):
    def __enter__(self) -> Platform:
        pygame.init()
        return self

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> Optional[bool]:
        pygame.quit()
        return None


def main() -> None:
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
