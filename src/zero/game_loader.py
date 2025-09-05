from abc import ABC, abstractmethod
from asyncio import Event, TaskGroup
from types import TracebackType

import pygame

from zero.contextmanagers import CONTEXT_MANAGER_EXIT_DO_NOT_SUPPRESS_EXCEPTION
from zero.display import Display, DisplayConfig
from zero.game import Game
from zero.resources.loader import ResourceLoader
from zero.type_wrappers.arithmetic import NonNegInt


class GameLoaderPostLoadPlugin(ABC):
    @abstractmethod
    async def send_commands(self, game: Game) -> None:
        """
        Post-load hook to instrument the game after it was successfully loaded.
        """


class GameLoader:
    def __init__(self, display_config: DisplayConfig) -> None:
        self._post_load_plugins: list[GameLoaderPostLoadPlugin] = []
        self._game: Game
        self._is_aenter_event: Event = Event()
        self._is_aexit_event: Event = Event()
        self._task_group: TaskGroup = TaskGroup()
        self._display_config = display_config

    async def __aenter__(self) -> Game:
        assert not self._is_aenter_event.is_set()
        assert not self._is_aexit_event.is_set()
        await self._task_group.__aenter__()
        self._is_aenter_event.set()
        try:
            await self._load_game()
            await self._run_post_load_plugins()
        except Exception as e:
            await self.__aexit__(type(e), e, e.__traceback__)
            raise
        else:
            return self._game

    async def _load_game(self) -> None:
        assert not pygame.get_init(), (
            "Supposed to not be initialized yet, did we forget to call "
            "pygame.quit() somewhere?"
        )
        pygame.init()
        self._game = Game(
            resource_loader=ResourceLoader(),
            fps=NonNegInt(240),
            display=Display(self._display_config),
            task_group=self._task_group,
        )
        await self._game.setup_mouse_cursor()
        self._task_group.create_task(self._game.game_loop_until_quit())
        await self._game.wait_loop_started()

    async def _run_post_load_plugins(self) -> None:
        for plugin in self._post_load_plugins:
            await plugin.send_commands(self._game)

    async def __aexit__(
        self,
        _exc_type: type[BaseException] | None,
        _exc_val: BaseException | None,
        _exc_tb: TracebackType | None,
    ) -> bool | None:
        assert self._is_aenter_event.is_set()
        assert not self._is_aexit_event.is_set()
        assert pygame.get_init()
        self._is_aexit_event.set()
        try:
            await self._game.try_send_quit()
            await self._game.wait_exit()
            return CONTEXT_MANAGER_EXIT_DO_NOT_SUPPRESS_EXCEPTION
        finally:
            pygame.quit()
            await self._task_group.__aexit__(None, None, None)

    def register_post_load_plugin(self, plugin: GameLoaderPostLoadPlugin) -> None:
        self._post_load_plugins.append(plugin)
