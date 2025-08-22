from functools import cached_property
from typing import cast

from zero.resources.sprites.cursor import MouseCursorSprite


class ResourceLoader:
    @cached_property
    def cursor_sprite(self) -> MouseCursorSprite:
        return MouseCursorSprite.load()

    @cached_property
    def convert_cursor_sprite(self) -> MouseCursorSprite:
        return cast(MouseCursorSprite, self.cursor_sprite.convert())

    @cached_property
    def convert_pressed_cursor_sprite(self) -> MouseCursorSprite:
        return cast(MouseCursorSprite, self.cursor_sprite.convert())
