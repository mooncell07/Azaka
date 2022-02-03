from __future__ import annotations

import asyncio

import azaka
import pytest


@pytest.mark.asyncio
async def test_connection() -> None:
    client = azaka.Client()
    old_state: asyncio.Queue[bool] = asyncio.Queue()

    @client.register
    async def inner(ctx: azaka.Context) -> None:
        await client.wait_until_connect()
        old_state.put_nowait(ctx.client.connected)
        client.stop()

    await client.connect()
    assert not old_state.empty()
    was_connected = old_state.get_nowait()
    assert was_connected
