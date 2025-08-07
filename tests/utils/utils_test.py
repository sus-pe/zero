from tests.utils import MockPlatform
from zero.core import ExitCommand


def test_mock_exit_command(mock_platform: MockPlatform):
    mock_platform.queue_exit_command()
    assert isinstance(mock_platform.get_pending_commands()[0], ExitCommand)
    assert len(mock_platform.get_pending_commands()) == 0
