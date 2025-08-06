from __future__ import annotations

from typing import Collection


from zero import Zero
from zero.core import Platform, NullCommand, Command


class DummyPlatform(Platform):
    def get_pending_commands(self) -> Collection:
        return []


class MockPlatform(DummyPlatform):
    def __init__(self, pending_commands: Collection[Command]) -> None:
        self._pending_commands = pending_commands

    def get_pending_commands(self) -> Collection:
        return self._pending_commands


def test_zero():
    Zero(platform=DummyPlatform()).process_pending_commands()


def test_mock_platform():
    expected_pending_commands = [NullCommand()]
    mock_platform = MockPlatform(pending_commands=expected_pending_commands)
    pending_commands = mock_platform.get_pending_commands()
    assert pending_commands is expected_pending_commands


def test_zero_process_command():
    z = Zero(platform=MockPlatform(pending_commands=[]))
    z.process_pending_commands()
