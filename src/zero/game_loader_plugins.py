from zero.game import Game
from zero.game_loader import GameLoaderPostLoadPlugin


class DefaultPostLoadPlugin(GameLoaderPostLoadPlugin):
    async def send_commands(self, game: Game) -> None:
        assert game, "Game is supposed to be initialized!"


class GameTestLoaderPostLoadPlugin(GameLoaderPostLoadPlugin):
    async def send_commands(self, game: Game) -> None:
        assert game, "Supposed to be initialized!"
        initial_state = game.display.is_fullscreen
        game.send_f11()
        await game.wait_next_loop()
        assert initial_state != game.display.is_fullscreen
        game.send_f11()
        await game.wait_next_loop()
        assert initial_state == game.display.is_fullscreen
        game.send_quit()
