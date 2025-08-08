import zero
import zero.pygame_adapter
from tests.integration.conftest import MockPygame


def test_main(mock_pygame: MockPygame) -> None:
    zero.pygame_adapter.main()
    mock_pygame.init.assert_called_once()
    mock_pygame.quit.assert_called_once()
