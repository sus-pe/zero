from collections.abc import Callable
from typing import Any

import pygame
from pygame import Surface

from tests.conftest import Fixture, fixture, raises
from zero.contextmanagers import (
    PygameContext,
    assert_raises,
    suppress_no_fast_renderer_warning,
)


def always_fail(e: type[BaseException], msg: str) -> None:
    raise e(msg)


def test_assert_raises() -> None:
    msg = "Stub Message"
    e = AssertionError
    with assert_raises(e, msg):
        always_fail(e, msg)

    with raises(AssertionError), assert_raises(e, msg):
        pass


def assert_warning(match: str, callback: Callable[[], Any]) -> None:
    with raises(Warning, match=match):
        callback()


type ScaledDisplayFactory = Callable[[], Surface]


@fixture
def scaled_display_factory(
    pygame_context: PygameContext,
) -> Fixture[ScaledDisplayFactory]:
    pygame_context.assert_init()

    def _factory() -> Surface:
        return pygame.display.set_mode((1, 1), flags=pygame.SCALED)

    yield _factory


def assert_fast_renderer_warning(callback: Callable[[], Any]) -> None:
    assert_warning("no fast renderer available", callback)


def test_pygame_no_fast_renderer_warning_suppressor(
    scaled_display_factory: ScaledDisplayFactory,
) -> None:
    assert_fast_renderer_warning(scaled_display_factory)

    with suppress_no_fast_renderer_warning():
        scaled_display_factory()

    assert_fast_renderer_warning(scaled_display_factory)
