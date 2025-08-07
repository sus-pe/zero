import sys
from importlib import reload

from zero.core import Platform


class DummyPlatform(Platform):
    pass


class MockPlatform(DummyPlatform):
    pass


def reload_modules(prefix: str) -> list[str]:
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
