from zero import __main__


async def test_sanity() -> None:
    await __main__.async_main(send_quit=True)
