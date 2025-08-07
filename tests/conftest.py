from pytest import fixture

from tests.utils import MockPlatform


@fixture
def mock_platform() -> MockPlatform:
    return MockPlatform()
