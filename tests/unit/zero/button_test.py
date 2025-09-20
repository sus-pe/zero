from zero.game import Game
from zero.type_wrappers.window import WindowXY


def test_button(game: Game) -> None:
    assert game.button_sprite
    button_xy = WindowXY.from_xy(10, 10)
    game.render(game.button_sprite, at=button_xy)
    assert game.is_displayed(game.button_sprite, xy=button_xy)
