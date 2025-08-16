from zero.game import Game


async def test_window_auto_with_event_driven(game: Game) -> None:
    game.assert_resizeable()
    await game.send_quit()
    await game.wait_exit()
