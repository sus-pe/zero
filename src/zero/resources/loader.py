from functools import cached_property
from typing import cast

from zero.resources.sprites.cursor import (
    ButtonSprite,
    MouseCursorSprite,
    PressedMouseCursorSprite,
)


class ResourceLoader:
    @cached_property
    def cursor_sprite(self) -> MouseCursorSprite:
        return MouseCursorSprite.load()

    @cached_property
    def pressed_cursor_sprite(self) -> PressedMouseCursorSprite:
        return PressedMouseCursorSprite.load()

    @cached_property
    def convert_cursor_sprite(self) -> MouseCursorSprite:
        return cast(MouseCursorSprite, self.cursor_sprite.convert())

    @cached_property
    def convert_pressed_cursor_sprite(self) -> PressedMouseCursorSprite:
        return cast(PressedMouseCursorSprite, self.pressed_cursor_sprite.convert())

    @cached_property
    def button_sprite(self) -> ButtonSprite:
        return ButtonSprite.load()

    @cached_property
    def convert_button_sprite(self) -> ButtonSprite:
        return cast(ButtonSprite, self.button_sprite.convert())
