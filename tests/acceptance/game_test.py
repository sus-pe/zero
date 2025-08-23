from zero.game import Game


async def test_game_fullscreen(game: Game) -> None:
    game.set_windowed()
    assert game.is_windowed()
    game.set_fullscreen()
    assert game.is_fullscreen()
    game.set_fullscreen()
    assert game.is_fullscreen()
    game.toggle_fullscreen()
    assert game.is_windowed()
    game.toggle_fullscreen()
    assert game.is_fullscreen()


async def test_game_fullscreen_button(game: Game) -> None:
    assert game.is_windowed()
    game.send_f11()
    await game.wait_next_loop()
    assert game.is_fullscreen()
    game.send_f11()
    await game.wait_next_loop()
    assert game.is_windowed()
