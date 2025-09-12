from zero.game import Game


def test_button(game: Game) -> None:
    assert game.button_sprite
