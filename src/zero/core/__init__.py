from abc import ABC


class Platform(ABC):
    pass


class Zero:
    def __init__(self, platform: Platform):
        assert isinstance(platform, Platform)
