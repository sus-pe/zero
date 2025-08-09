import logging
from collections.abc import Generator
from contextlib import contextmanager
from types import TracebackType

import pygame

from zero.core import IO, DisplaySettings, GameLoop
from zero.core.types import DisplayResolution


class PygameConductor:
    def __init__(self, io: IO) -> None:
        self._io = io

    def __enter__(self) -> "PygameConductor":
        pygame.init()
        pygame.display.set_mode(self._io.display_settings.resolution)
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> bool | None:
        pygame.quit()
        return None

    @classmethod
    @contextmanager
    def main(cls) -> Generator["PygameConductor", None, None]:
        logger = logging.getLogger()
        default_display_settings = DisplaySettings(DisplayResolution.SD_4_3)
        io = IO(default_display_settings)

        with PygameConductor(io) as game_conductor:
            yield game_conductor

            zero = GameLoop(io=io)
            io.queue_exit_command()
            zero.loop_until_exit_command()

            logger.info(DisplayResolution.SD_4_3)
            logger.info(DisplayResolution.FHD_1080P)
            logger.info(DisplayResolution.HD_720P)
            logger.info(DisplayResolution.QHD_1440P)
            logger.info(DisplayResolution.UHD_4K)
            logger.info(DisplayResolution.UWQHD_21_9)
