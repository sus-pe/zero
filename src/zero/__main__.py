import asyncio

import typer

from zero.game_loader import GameLoader


async def async_main(
    *,
    resizeable: bool,
    scaled: bool,
    send_quit: bool = False,
) -> int:
    async with GameLoader(resizeable=resizeable, scaled=scaled) as game:
        if send_quit:
            await game.send_quit()
        await game.wait_exit()
    return 0


def main(
    *, send_quit: bool = False, resizeable: bool = True, scaled: bool = True
) -> int:
    # pragma: no cover
    return asyncio.run(
        async_main(
            send_quit=send_quit,
            resizeable=resizeable,
            scaled=scaled,
        )
    )


if __name__ == "__main__":  # pragma: no cover
    typer.run(main)
