import sys
from typing import Any, Generator
from unittest.mock import MagicMock
from importlib import reload
from pytest import fixture, FixtureRequest

import zero
import zero.pygame


def reload_modules(prefix: str):
    """
    Reload all modules that start with the given prefix (e.g. 'zero.').
    This is safer than trying to reload all modules in sys.modules.
    """
    reloaded = []
    for name in list(sys.modules.keys()):
        if name == prefix or name.startswith(prefix + "."):
            mod = sys.modules.get(name)
            if mod is not None:
                reload(mod)
                reloaded.append(name)
    return reloaded


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
