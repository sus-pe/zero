from zero.resources.loader import ResourceLoader
from zero.type_wrappers.arithmetic import Bit

COUNT_ONLY_FLAG: Bit = Bit.zero


def test_transform_threshold(resource_loader: ResourceLoader) -> None:
    sprite = resource_loader.cursor_sprite
    sub = sprite.subsprite(sprite.rect)
    assert sprite.is_displayed_by(sub)
    assert not sprite.is_displayed_by(sprite.subsprite(sprite.rect.inflate(-1, -1)))
