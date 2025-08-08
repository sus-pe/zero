import zero
import zero.pygame
from tests.integration.conftest import MockPygame


def test_main(mock_pygame: MockPygame) -> None:
    zero.pygame.main()
    mock_pygame.init.assert_called_once()
    mock_pygame.quit.assert_called_once()
