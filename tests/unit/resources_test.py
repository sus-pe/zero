from pytest import fixture

from zero.resources.fetcher import ResourceFetcher


@fixture
def fetcher() -> ResourceFetcher:
    return ResourceFetcher()


def test_resources(fetcher: ResourceFetcher) -> None:
    assert fetcher.get_cursor_sprite().is_file()
