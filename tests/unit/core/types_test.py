from pytest import raises

from zero.core.types import DisplayResolution, Pixels, Resolution


def test_pixel() -> None:
    v = 640
    pixels = Pixels(v)
    assert int(pixels) == v

    bad_pixels = -640
    with raises(ValueError):
        Pixels(bad_pixels)

    with raises(ValueError):
        Pixels(0)

    assert Pixels(1920) / Pixels(1080) == 1920 / 1080


def test_resolution() -> None:
    expected_width = 640
    expected_height = 640
    r = Resolution(width=Pixels(expected_width), height=Pixels(expected_height))
    assert r[0] == expected_width
    assert r[1] == expected_height

    with raises(IndexError):
        r[2]

    expected_length = 2
    assert len(r) == expected_length
    assert r.aspect_ratio == r.width / r.height


def test_default_resolutions() -> None:
    for r in DisplayResolution:
        width, height = r
        assert width == r.value.width
        assert height == r.value.height
        assert width == r.width
        assert height == r.height
        assert r.aspect_ratio == r.value.aspect_ratio
        assert repr(r)
