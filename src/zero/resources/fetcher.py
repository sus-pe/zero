from pathlib import Path

from zero.resources.sprites.cursor import CURSOR_PATH


class ResourceFetcher:
    def get_cursor_sprite(self) -> Path:
        return CURSOR_PATH
