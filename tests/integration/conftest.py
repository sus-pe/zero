import sys
from collections.abc import Generator
from typing import Any
from unittest.mock import MagicMock

from pytest import fixture

import zero
import zero.pygame_adapter
from tests.utils import reload_modules


class MockPygame(MagicMock):
    pass


@fixture
def mock_pygame() -> Generator[MockPygame, Any, None]:
    mock_pygame = MockPygame()
    cached_pygame = sys.modules["pygame"]
    try:
        sys.modules["pygame"] = mock_pygame
        reload_modules(zero.pygame_adapter.__name__)
        yield mock_pygame
    finally:
        sys.modules["pygame"] = cached_pygame
        reload_modules(zero.pygame_adapter.__name__)
