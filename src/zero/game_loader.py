from asyncio import Event, create_task
from types import TracebackType

import pygame

from zero.contextmanagers import CONTEXT_MANAGER_EXIT_DO_NOT_SUPPRESS_EXCEPTION
from zero.game import Game
from zero.resources.loader import ResourceLoader
from zero.type_wrappers.arithmetic import NonNegInt


class GameLoader:
    def __init__(self, *, resizeable: bool = True, scaled: bool = True) -> None:
        self._game: Game
        self._is_started_event: Event = Event()
        self._is_aexit_event: Event = Event()
        self._display_flags = pygame.RESIZABLE if resizeable else 0
        self._display_flags |= pygame.SCALED if scaled else 0

    async def __aenter__(self) -> Game:
        assert not self._is_started_event.is_set()
        self._game = Game(resource_loader=ResourceLoader(), fps=NonNegInt(240))
        self._is_started_event.set()
        pygame.init()
        await self._game.setup_display(flags=self._display_flags)
        await self._game.setup_mouse_cursor()
        self._game_task = create_task(self._game.game_loop_until_quit())
        await self._game.wait_loop_started()
        return self._game

    async def __aexit__(
        self,
        _exc_type: type[BaseException] | None,
        _exc_val: BaseException | None,
        _exc_tb: TracebackType | None,
    ) -> bool | None:
        assert self._is_started_event.is_set()
        await self._game.try_send_quit()
        await self._game.wait_exit()
        pygame.quit()
        assert self._game_task, "Supposed to be initialized"
        await self._game_task
        return CONTEXT_MANAGER_EXIT_DO_NOT_SUPPRESS_EXCEPTION
