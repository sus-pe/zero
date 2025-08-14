from os import environ

from pytest import fixture


@fixture(scope="session", autouse=True)
def sdl_headless_env() -> None:
    # Must be set before pygame.init()
    environ.setdefault("SDL_VIDEODRIVER", "dummy")
