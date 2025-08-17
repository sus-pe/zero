from functools import cached_property

from zero.resources.sprites.cursor import MouseCursorSprite


class ResourceLoader:
    @cached_property
    def cursor_sprite(self) -> MouseCursorSprite:
        return MouseCursorSprite.load()
