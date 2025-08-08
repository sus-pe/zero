from unittest.mock import MagicMock

from zero.pygame import PygameIO


def test_pygame(mock_pygame: MagicMock) -> None:
    with PygameIO() as platform:
        assert platform
        mock_pygame.init.assert_called_once()
    mock_pygame.quit.assert_called_once()
