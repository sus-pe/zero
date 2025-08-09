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
    expected_width = Pixels(640)
    expected_height = Pixels(640)
    r = Resolution(width=expected_width, height=expected_height)
    assert r[0] == expected_width
    assert r[1] == expected_height

    with raises(IndexError):
        r[2]

    expected_length = 2
    assert len(r) == expected_length
    assert r.aspect_ratio == r.width / r.height


def test_default_resolutions() -> None:
    for r in DisplayResolution:
        assert repr(r)
        assert len(r) == len(r.value)
        assert r[0] == float(r.width)
        assert r[1] == float(r.height)
