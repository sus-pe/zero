from __future__ import annotations

from _pytest.fixtures import fixture

from tests.utils import MockPlatform


@fixture
def mock_platform() -> MockPlatform:
    return MockPlatform()
