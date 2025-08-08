import sys
from typing import Any, Generator
from unittest.mock import MagicMock

from pytest import FixtureRequest, fixture

import zero
import zero.pygame
from tests.utils import reload_modules


class MockPygame(MagicMock):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        # Nice-to-have name for clearer tracebacks
        kwargs.setdefault("name", "pygame")
        super().__init__(*args, **kwargs)


@fixture
def mock_pygame(request: FixtureRequest) -> Generator[MockPygame, Any, None]:
    mock_pygame = MockPygame()
    cached_pygame = sys.modules["pygame"]
    try:
        sys.modules["pygame"] = mock_pygame
        reload_modules(zero.pygame.__name__)
        yield mock_pygame
    finally:
        sys.modules["pygame"] = cached_pygame
        reload_modules(zero.pygame.__name__)
