import asyncio
import sys

from zero.game import Game


async def main() -> int:  # pragma: no cover
    async with Game() as game:
        await game.start_game()
    return 0


if __name__ == "__main__":  # pragma: no cover
    sys.exit(asyncio.run(main()))
