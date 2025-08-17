from pytest import fixture

from zero.resources.loader import ResourceLoader


@fixture
def fetcher() -> ResourceLoader:
    return ResourceLoader()


def test_resources(fetcher: ResourceLoader) -> None:
    sprite = fetcher.cursor_sprite
    assert sprite.width
    assert sprite.height
