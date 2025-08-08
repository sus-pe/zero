import random
import string
import sys
from collections.abc import Generator
from dataclasses import dataclass
from types import ModuleType
from unittest.mock import MagicMock

from pytest import MonkeyPatch, fixture

from zero.core import IO, DisplaySettings, GameLoop
from zero.core.types import DisplayResolution


@fixture
def display_resolution() -> DisplayResolution:
    return DisplayResolution.SD_4_3


@fixture
def display_settings(display_resolution: DisplayResolution) -> DisplaySettings:
    return DisplaySettings(display_resolution.value)


@fixture
def zero(io: IO) -> GameLoop:
    return GameLoop(io=io)


@fixture
def io(display_settings: DisplaySettings) -> IO:
    return IO(display_settings)


class MockReload(MagicMock):
    @property
    def reloaded_modules(self) -> set[str]:
        return {call.args[0].__name__ for call in self.call_args_list}


def register_fake_modules(module_names: set[str]) -> None:
    for name in module_names:
        sys.modules[name] = ModuleType(name)


@fixture(scope="session", autouse=True)
def fixed_random_seed() -> int:
    seed = 42
    random.seed(seed)
    return seed


@fixture(scope="session")
def package_suffix_length() -> int:
    return 8


@fixture
def fake_package_prefix(package_suffix_length: int) -> str:
    suffix = "".join(
        random.choices(string.ascii_lowercase + string.digits, k=package_suffix_length),
    )
    return f"pkg_{suffix}"


@fixture
def fake_package_names(fake_package_prefix: str) -> set[str]:
    return {
        f"{fake_package_prefix}",
        f"{fake_package_prefix}.utils",
        f"{fake_package_prefix}.sub.module",
    }


def create_fake_module(name: str) -> ModuleType:
    return ModuleType(name)


@dataclass(frozen=True)
class FakeModules:
    prefix: str
    module_names: set[str]


@fixture
def fake_modules(
    fake_package_prefix: str,
    fake_package_names: set[str],
) -> Generator[FakeModules, None, None]:
    original_sys_modules = sys.modules.copy()

    # Register expected modules
    register_fake_modules(fake_package_names)
    sys.modules["unrelated.module"] = create_fake_module("unrelated.module")

    try:
        yield FakeModules(fake_package_prefix, fake_package_names)
    finally:
        sys.modules.clear()
        sys.modules.update(original_sys_modules)


@fixture
def mock_reload(monkeypatch: MonkeyPatch) -> MockReload:
    mock = MockReload()
    monkeypatch.setitem(
        sys.modules,
        "importlib",
        sys.modules.get("importlib"),
    )  # ensure it exists
    monkeypatch.setattr("tests.utils.reload", mock)
    return mock
