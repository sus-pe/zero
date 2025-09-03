from os import environ

from zero.sdl import (
    SDL_AUDIODRIVER_ENV_KEY,
    SDL_VIDEODRIVER_ENV_KEY,
    with_dummy_sdl_env,
    with_hw_sdl_env,
)


def assert_video_is(value: str) -> None:
    assert environ.get(SDL_VIDEODRIVER_ENV_KEY) == value


def assert_video_unset() -> None:
    assert SDL_VIDEODRIVER_ENV_KEY not in environ


def assert_audio_is(value: str) -> None:
    assert environ.get(SDL_AUDIODRIVER_ENV_KEY) == value


def assert_audio_unset() -> None:
    assert SDL_AUDIODRIVER_ENV_KEY not in environ


def test_with_dummy_sdl_env_forces_dummy() -> None:
    environ[SDL_VIDEODRIVER_ENV_KEY] = "real_video"
    environ[SDL_AUDIODRIVER_ENV_KEY] = "real_audio"

    with with_dummy_sdl_env() as (v, a):
        assert (v, a) == ("dummy", "dummy")
        assert_video_is("dummy")
        assert_audio_is("dummy")

    assert_video_is("real_video")
    assert_audio_is("real_audio")


def test_with_hw_sdl_env_uses_real() -> None:
    environ[SDL_VIDEODRIVER_ENV_KEY] = "real_video"
    environ[SDL_AUDIODRIVER_ENV_KEY] = "real_audio"

    with with_hw_sdl_env() as (v, a):
        assert (v, a) == ("real_video", "real_audio")
        assert_video_is("real_video")
        assert_audio_is("real_audio")

    assert_video_is("real_video")
    assert_audio_is("real_audio")


def test_with_hw_sdl_env_removes_dummy() -> None:
    environ[SDL_VIDEODRIVER_ENV_KEY] = "dummy"
    environ[SDL_AUDIODRIVER_ENV_KEY] = "dummy"

    with with_hw_sdl_env() as (v, a):
        assert (v, a) == ("auto", "auto")
        assert_video_unset()
        assert_audio_unset()

    assert_video_is("dummy")
    assert_audio_is("dummy")


def test_with_hw_sdl_env_handles_missing() -> None:
    environ.pop(SDL_VIDEODRIVER_ENV_KEY, None)
    environ.pop(SDL_AUDIODRIVER_ENV_KEY, None)

    with with_hw_sdl_env() as (v, a):
        assert (v, a) == ("auto", "auto")
        assert_video_unset()
        assert_audio_unset()

    assert_video_unset()
    assert_audio_unset()


def test_sdl_hw_driver_fixture(sdl_hw_driver: str) -> None:
    assert sdl_hw_driver == "video='auto' audio='auto'"
    assert_audio_unset()
    assert_video_unset()


def test_sdl_headless_env_fixture(sdl_headless_env: str) -> None:
    assert sdl_headless_env == "video='dummy' audio='dummy'"
    assert_video_is("dummy")
    assert_audio_is("dummy")
