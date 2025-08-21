import asyncio

import typer

from zero.game import Game


async def async_main(*, send_quit: bool = False) -> int:
    async with Game() as game:
        if send_quit:
            await game.send_quit()
        await game.wait_exit()
    return 0


def main(*, send_quit: bool = False) -> int:  # pragma: no cover
    return asyncio.run(async_main(send_quit=send_quit))


if __name__ == "__main__":  # pragma: no cover
    typer.run(main)
