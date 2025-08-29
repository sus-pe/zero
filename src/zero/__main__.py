import asyncio
from dataclasses import dataclass
from types import TracebackType

import typer

from zero import safe_asyncio
from zero.contextmanagers import CONTEXT_MANAGER_EXIT_DO_NOT_SUPPRESS_EXCEPTION
from zero.display import DisplayConfig
from zero.game import Game
from zero.game_loader import GameLoader, GameLoaderPostLoadPlugin


@dataclass(frozen=True)
class MainConfig:
    display: DisplayConfig


class Main:
    def __init__(
        self,
        game_loader: GameLoader,
    ) -> None:
        self._loader = game_loader

    async def main(self) -> int:
        await self._load_game_and_wait_exit()
        return 0

    async def _load_game_and_wait_exit(
        self,
    ) -> None:
        async with self._loader as game:
            await game.wait_exit()

    @classmethod
    def create_from(
        cls, config: MainConfig, *plugins: GameLoaderPostLoadPlugin
    ) -> "Main":
        loader = GameLoader(display_config=config.display)
        for plugin in plugins:
            loader.register(plugin)
        return Main(
            game_loader=loader,
        )


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


class DefaultPostLoadPlugin(GameLoaderPostLoadPlugin):
    async def send_commands(self, game: Game) -> None:
        assert game, "Game is supposed to be initialized!"


class AsyncLeakDetector:
    async def __aenter__(self) -> "AsyncLeakDetector":
        self.loop = asyncio.get_running_loop()
        self.before = set(asyncio.all_tasks(self.loop))
        return self

    async def __aexit__(
        self,
        _exc_type: type[BaseException] | None,
        _exc_val: BaseException | None,
        _exc_tb: TracebackType | None,
    ) -> bool | None:
        after = set(asyncio.all_tasks(self.loop)) - self.before
        leaked = [t for t in after if not t.done()]
        assert not leaked, f"Leaked: {leaked}"
        return CONTEXT_MANAGER_EXIT_DO_NOT_SUPPRESS_EXCEPTION


async def main(
    *,
    is_test: bool = False,
    is_hidden: bool = False,
    is_fullscreen: bool = True,
    is_scaled: bool = True,
    post_load_plugin: GameLoaderPostLoadPlugin | None = None,
) -> int:
    async with AsyncLeakDetector():
        display = DisplayConfig(
            is_scaled=is_scaled,
            is_hidden=is_hidden,
            is_fullscreen=is_fullscreen,
        )
        test_plugin = (
            GameTestLoaderPostLoadPlugin() if is_test else DefaultPostLoadPlugin()
        )
        post_load_plugin = (
            post_load_plugin if post_load_plugin else DefaultPostLoadPlugin()
        )
        config = MainConfig(display)
        return await Main.create_from(config, test_plugin, post_load_plugin).main()


def _cli_main(
    *,
    is_test: bool = False,
    is_hidden: bool = False,
    is_fullscreen: bool = True,
    is_scaled: bool = True,
) -> int:
    return safe_asyncio.run(
        main(
            is_test=is_test,
            is_fullscreen=is_fullscreen,
            is_hidden=is_hidden,
            is_scaled=is_scaled,
        )
    )


if __name__ == "__main__":  # pragma: no cover
    typer.run(_cli_main)
