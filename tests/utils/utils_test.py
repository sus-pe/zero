from tests.conftest import FakeModules, MockReload, register_fake_modules
from tests.utils import MockPlatform, reload_modules
from zero.core import ExitCommand


def test_mock_exit_command(mock_platform: MockPlatform) -> None:
    mock_platform.queue_exit_command()
    assert isinstance(mock_platform.get_pending_commands()[0], ExitCommand)
    assert len(mock_platform.get_pending_commands()) == 0


def test_reload_modules_only_reloads_matching_prefix(
    mock_reload: MockReload,
    fake_modules: FakeModules,
) -> None:
    unrelated_modules = {"unrelated.module"}
    register_fake_modules(fake_modules.module_names | unrelated_modules)

    reloaded = reload_modules(fake_modules.prefix)

    assert set(reloaded) == fake_modules.module_names
    assert mock_reload.reloaded_modules == fake_modules.module_names, (
        f"Expected reload calls for: {fake_modules.module_names}, but got: {mock_reload.reloaded_modules}"
    )
