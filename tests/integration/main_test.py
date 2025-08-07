from unittest.mock import MagicMock
import zero
import zero.pygame


def test_main(mock_pygame: MagicMock):
    zero.pygame.main()
    mock_pygame.init.assert_called_once()
