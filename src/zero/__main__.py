from dataclasses import dataclass, replace
from typing import ClassVar

import typer

from zero import safe_asyncio
from zero.contextmanagers import PygameContext
from zero.display import DisplayConfig
from zero.game_loader import GameLoader, GameLoaderPostLoadPlugin
from zero.game_loader_plugins import DefaultPostLoadPlugin, GameTestLoaderPostLoadPlugin
from zero.logger import create_for
from zero.safe_asyncio import AsyncLeakDetector
from zero.support import CompositeSupport, LoggerSupport, Support

logger = create_for(__file__)


@dataclass(frozen=True)
class MainArgs:
    is_scaled: bool
    is_hidden: bool
    is_fullscreen: bool
    is_allow_no_fast_renderer: bool
    is_test: bool

    TEST: ClassVar["MainArgs"]
    PROD: ClassVar["MainArgs"]

    def override(self, **kwargs: bool | None) -> "MainArgs":
        sanitized_kwargs = {k: v for k, v in kwargs.items() if v is not None}
        return replace(
            self,
            **sanitized_kwargs,
        )


MainArgs.TEST = MainArgs(
    is_test=True,
    is_scaled=False,
    is_hidden=True,
    is_fullscreen=False,
    is_allow_no_fast_renderer=False,
)

MainArgs.PROD = MainArgs(
    is_test=False,
    is_scaled=True,
    is_hidden=False,
    is_fullscreen=True,
    is_allow_no_fast_renderer=False,
)


@dataclass(frozen=True)
class MainConfig:
    display: DisplayConfig
    post_load_plugins: list[GameLoaderPostLoadPlugin]
    support: Support

    @classmethod
    def create_from(
        cls,
        *,
        args: MainArgs,
        post_load_plugin: GameLoaderPostLoadPlugin | None,
        support: Support | None,
    ) -> "MainConfig":
        display = DisplayConfig(
            is_scaled=args.is_scaled,
            is_hidden=args.is_hidden,
            is_fullscreen=args.is_fullscreen,
            is_allow_no_fast_renderer=args.is_allow_no_fast_renderer,
        )
        test_plugin = (
            GameTestLoaderPostLoadPlugin() if args.is_test else DefaultPostLoadPlugin()
        )
        post_load_plugin = (
            post_load_plugin if post_load_plugin else DefaultPostLoadPlugin()
        )

        support = support if support else LoggerSupport(logger)
        supports = CompositeSupport(support)

        return MainConfig(display, [test_plugin, post_load_plugin], supports)


class Main:
    async def main(self, config: MainConfig) -> int:
        try:
            async with AsyncLeakDetector():
                await self._load_game_and_wait_exit(
                    config.display, config.post_load_plugins
                )
        except BaseException as e:
            config.support.notify_crashed(e)
            raise
        else:
            return 0

    async def _load_game_and_wait_exit(
        self,
        display: DisplayConfig,
        post_load_plugins: list[GameLoaderPostLoadPlugin],
    ) -> None:
        with PygameContext() as context:
            loader = GameLoader(display, context, post_load_plugins)

            async with loader as game:
                await game.wait_exit()


async def main(
    args: MainArgs,
    *,
    post_load_plugin: GameLoaderPostLoadPlugin | None = None,
    support: Support | None = None,
) -> int:
    config = MainConfig.create_from(
        args=args,
        post_load_plugin=post_load_plugin,
        support=support,
    )
    return await Main().main(config)


async def main_test(
    support: Support,
    test_args: MainArgs = MainArgs.TEST,
    post_load_plugin: GameLoaderPostLoadPlugin | None = None,
) -> int:
    return await main(
        support=support,
        args=test_args,
        post_load_plugin=post_load_plugin,
    )


def cli_main(
    *,
    is_test: bool | None = None,
    is_hidden: bool | None = None,
    is_fullscreen: bool | None = None,
    is_scaled: bool | None = None,
    is_allow_no_fast_renderer: bool | None = None,
) -> int:
    args = MainArgs.TEST if is_test else MainArgs.PROD
    args = args.override(
        is_scaled=is_scaled,
        is_hidden=is_hidden,
        is_fullscreen=is_fullscreen,
        is_allow_no_fast_renderer=is_allow_no_fast_renderer,
    )
    return safe_asyncio.run(main(args))


if __name__ == "__main__":  # pragma: no cover
    typer.run(cli_main)
