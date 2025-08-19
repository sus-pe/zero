from zero.resources.loader import ResourceLoader
from zero.type_wrappers.window import WindowXY


def test_resources(resource_loader: ResourceLoader) -> None:
    sprite = resource_loader.cursor_sprite
    assert sprite.width
    assert sprite.height
    assert sprite.as_np is not None
    assert sprite.rect
    assert sprite.rect_at(WindowXY.from_xy(2, 1))
