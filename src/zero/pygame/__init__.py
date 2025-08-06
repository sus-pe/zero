from typing import Collection

from zero.core import Platform, NullCommand


class PygamePlatform(Platform):
    def get_pending_commands(self) -> Collection:
        return [NullCommand()]
