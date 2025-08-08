import logging
from types import TracebackType

import pygame

from zero.core import DisplaySettings, Platform, Zero
from zero.core.types import DisplayResolution


class PygamePlatform(Platform):
    def __enter__(self) -> Platform:
        pygame.init()
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> bool | None:
        pygame.quit()
        return None


def main() -> None:
    logger = logging.getLogger()
    with PygamePlatform() as io:
        io.set_display_settings(DisplaySettings(DisplayResolution.SD_4_3.value))
        zero = Zero(platform=io, display_resolution=DisplayResolution.FHD_1080P.value)
        zero.display_init()
        logger.info(io.get_display_settings())
        zero.loop_for(3)
        io.queue_exit_command()
        zero.loop_until_exit_command()

        logger.info(DisplayResolution.SD_4_3)
        logger.info(DisplayResolution.FHD_1080P)
        logger.info(DisplayResolution.HD_720P)
        logger.info(DisplayResolution.QHD_1440P)
        logger.info(DisplayResolution.UHD_4K)
        logger.info(DisplayResolution.UWQHD_21_9)
