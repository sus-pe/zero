from unittest.mock import MagicMock

from zero.core import DisplaySettings
from zero.pygame import PygameIO


def test_pygame(mock_pygame: MagicMock, display_settings: DisplaySettings) -> None:
    with PygameIO(display_settings) as platform:
        assert platform
        mock_pygame.init.assert_called_once()
    mock_pygame.quit.assert_called_once()
