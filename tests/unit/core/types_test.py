from zero.core.types import Pixels, DisplayResolution
from zero.core.types import Resolution
from pytest import raises


def test_pixel():
    pixels = Pixels(640)

    with raises(ValueError):
        Pixels(-640)

    assert int(pixels) == 640

    assert Pixels(1920) / Pixels(1080) == 1920 / 1080


def test_resolution():
    r = Resolution(width=Pixels(640), height=Pixels(640))
    assert r[0] == 640
    assert r[1] == 640

    with raises(IndexError):
        r[2]

    assert len(r) == 2
    assert r.aspect_ratio == r.width / r.height


def test_default_resolutions():
    for r in DisplayResolution:
        width, height = r
        assert width == r.value.width
        assert height == r.value.height
        assert width == r.width
        assert height == r.height
        assert r.aspect_ratio == r.value.aspect_ratio
        assert repr(r)
