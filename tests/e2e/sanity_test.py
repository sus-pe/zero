import asyncio

import pygame
import pytest

from zero.__main__ import open_and_close_window


@pytest.mark.asyncio
async def test_window_auto_with_event_driven() -> None:
    is_started_event: asyncio.Event = asyncio.Event()

    window_task: asyncio.Task = asyncio.create_task(
        open_and_close_window(is_started_event),
    )
    await is_started_event.wait()

    pygame.event.post(pygame.event.Event(pygame.QUIT))
    await window_task
