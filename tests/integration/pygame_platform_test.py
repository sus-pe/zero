from unittest.mock import MagicMock

from zero.pygame import PygamePlatform


def test_pygame(mock_pygame: MagicMock) -> None:
    with PygamePlatform() as platform:
        assert platform
        mock_pygame.init.assert_called_once()
    mock_pygame.quit.assert_called_once()
