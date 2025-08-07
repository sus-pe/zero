import sys
from typing import Any, Generator
from unittest.mock import MagicMock

from pytest import FixtureRequest, fixture

import zero
import zero.pygame
from tests.utils import reload_modules


@fixture
def mock_pygame(request: FixtureRequest) -> Generator[MagicMock, Any, None]:
    mock_pygame = MagicMock()
    cached_pygame = sys.modules["pygame"]
    try:
        sys.modules["pygame"] = mock_pygame
        reload_modules(zero.pygame.__name__)
        yield mock_pygame
    finally:
        sys.modules["pygame"] = cached_pygame
        reload_modules(zero.pygame.__name__)
