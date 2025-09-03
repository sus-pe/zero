from collections.abc import Iterator
from contextlib import contextmanager
from os import environ

SDL_VIDEODRIVER_ENV_KEY: str = "SDL_VIDEODRIVER"
SDL_AUDIODRIVER_ENV_KEY: str = "SDL_AUDIODRIVER"


@contextmanager
def preserve_sdl_env() -> Iterator[None]:
    prev_video: str | None = environ.get(SDL_VIDEODRIVER_ENV_KEY)
    prev_audio: str | None = environ.get(SDL_AUDIODRIVER_ENV_KEY)
    try:
        yield
    finally:
        if prev_video is None:
            environ.pop(SDL_VIDEODRIVER_ENV_KEY, None)
        else:
            environ[SDL_VIDEODRIVER_ENV_KEY] = prev_video

        if prev_audio is None:
            environ.pop(SDL_AUDIODRIVER_ENV_KEY, None)
        else:
            environ[SDL_AUDIODRIVER_ENV_KEY] = prev_audio


def _ensure_not_dummy(key: str, fallback: str) -> str:
    val: str | None = environ.get(key)
    if val == "dummy":
        environ.pop(key, None)
        return fallback
    return val or fallback


@contextmanager
def with_dummy_sdl_env() -> Iterator[tuple[str, str]]:
    with preserve_sdl_env():
        environ[SDL_VIDEODRIVER_ENV_KEY] = "dummy"
        environ[SDL_AUDIODRIVER_ENV_KEY] = "dummy"
        yield "dummy", "dummy"


@contextmanager
def with_hw_sdl_env() -> Iterator[tuple[str, str]]:
    with preserve_sdl_env():
        video: str = _ensure_not_dummy(SDL_VIDEODRIVER_ENV_KEY, "auto")
        audio: str = _ensure_not_dummy(SDL_AUDIODRIVER_ENV_KEY, "auto")
        yield video, audio
