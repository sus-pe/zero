from types import TracebackType

from zero.contextmanagers import CONTEXT_MANAGER_EXIT_DO_NOT_SUPPRESS_EXCEPTION
from zero.game import Game


class GameLoader:
    def __init__(self) -> None:
        self._game: Game

    async def __aenter__(self) -> Game:
        self._game = await Game().__aenter__()
        return self._game

    async def __aexit__(
        self,
        _exc_type: type[BaseException] | None,
        _exc_val: BaseException | None,
        _exc_tb: TracebackType | None,
    ) -> bool | None:
        await self._game.__aexit__(_exc_type, _exc_val, _exc_tb)
        return CONTEXT_MANAGER_EXIT_DO_NOT_SUPPRESS_EXCEPTION
