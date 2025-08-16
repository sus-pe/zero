from typing import Any, cast

from pygame import MOUSEMOTION
from pygame import Event as PygameEvent

from zero.type_wrappers.typed_dict import PygameEventDict, PygameMouseMotionEventDict

PygameEventTypeCode = int
PygameMouseMotionEvent = PygameEvent


class PygameEventFactory:
    @classmethod
    def from_typed_dict(
        cls, event_type: PygameEventTypeCode, event_dict: PygameEventDict
    ) -> PygameEvent:
        return PygameEvent(
            event_type,
            cast(dict[str, Any], event_dict),
        )

    @classmethod
    def mouse_motion(cls, event: PygameMouseMotionEventDict) -> PygameMouseMotionEvent:
        return PygameEventFactory.from_typed_dict(
            event_type=MOUSEMOTION,
            event_dict=event,
        )
