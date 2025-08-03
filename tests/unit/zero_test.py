from __future__ import annotations

import pytest
from zero.builtins import NonNegativeInt
from zero.builtins import Pixels
from zero.builtins import Resolution
from zero.core import Zero, Platform


def test():
    pass


def test_positive_int():
    p = NonNegativeInt(1)
    assert p + 1 == 2
    with pytest.raises(ValueError):
        NonNegativeInt(-1)


def test_pixel():
    p = Pixels(640)
    assert p + 1 == 641
    with pytest.raises(ValueError):
        Pixels(-640)


def test_resolution():
    Resolution(width=Pixels(640), height=Pixels(640))


def test_resource():
    from importlib.resources import files

    resource_dir = files("zero.resources")
    assert resource_dir.is_dir()

    sprites_dir = resource_dir.joinpath("sprites")
    assert sprites_dir.is_dir()

    potato_sprite = sprites_dir.joinpath("potato.png")
    assert potato_sprite.is_file()

    audio_dir = resource_dir.joinpath("audio")
    assert audio_dir.is_dir()

    clank_sound = audio_dir.joinpath("clank.wav")
    assert clank_sound.is_file()


def test_zero():
    class DummyPlatform(Platform):
        pass

    Zero(platform=DummyPlatform())
