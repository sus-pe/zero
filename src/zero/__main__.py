from dataclasses import dataclass

import typer

from zero import safe_asyncio
from zero.display import DisplayConfig
from zero.game_loader import GameLoader, GameLoaderPostLoadPlugin
from zero.game_loader_plugins import DefaultPostLoadPlugin, GameTestLoaderPostLoadPlugin
from zero.safe_asyncio import AsyncLeakDetector


@dataclass(frozen=True)
class MainConfig:
    display: DisplayConfig
    post_load_plugins: list[GameLoaderPostLoadPlugin]


class Main:
    def __init__(
        self,
        game_loader: GameLoader,
    ) -> None:
        self._loader = game_loader

    async def main(self) -> int:
        async with AsyncLeakDetector():
            await self._load_game_and_wait_exit()
        return 0

    async def _load_game_and_wait_exit(
        self,
    ) -> None:
        async with self._loader as game:
            await game.wait_exit()

    @classmethod
    def create_from(cls, config: MainConfig) -> "Main":
        loader = GameLoader(display_config=config.display)
        for plugin in config.post_load_plugins:
            loader.register_post_load_plugin(plugin)
        return Main(
            game_loader=loader,
        )


async def main(
    *,
    is_test: bool = False,
    is_hidden: bool = False,
    is_fullscreen: bool = True,
    is_scaled: bool = True,
    is_allow_no_fast_renderer: bool = False,
    post_load_plugin: GameLoaderPostLoadPlugin | None = None,
) -> int:
    display = DisplayConfig(
        is_scaled=is_scaled,
        is_hidden=is_hidden,
        is_fullscreen=is_fullscreen,
        is_allow_no_fast_renderer=is_allow_no_fast_renderer,
    )
    test_plugin = GameTestLoaderPostLoadPlugin() if is_test else DefaultPostLoadPlugin()
    post_load_plugin = post_load_plugin if post_load_plugin else DefaultPostLoadPlugin()
    config = MainConfig(display, [test_plugin, post_load_plugin])
    return await Main.create_from(config).main()


def _cli_main(
    *,
    is_test: bool = False,
    is_hidden: bool = False,
    is_fullscreen: bool = True,
    is_scaled: bool = True,
    is_allow_no_fast_renderer: bool = False,
) -> int:
    return safe_asyncio.run(
        main(
            is_test=is_test,
            is_fullscreen=is_fullscreen,
            is_hidden=is_hidden,
            is_scaled=is_scaled,
            is_allow_no_fast_renderer=is_allow_no_fast_renderer,
        )
    )


if __name__ == "__main__":  # pragma: no cover
    typer.run(_cli_main)
