from __future__ import annotations

import asyncio
import typing as t

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


@pytest.mark.asyncio
async def test_vn() -> None:
    client = azaka.Client()
    results: asyncio.Queue[t.Optional[t.List[azaka.objects.VN]]] = asyncio.Queue()

    @client.register
    async def inner(ctx: azaka.Context) -> None:
        try:
            vn = await ctx.get_vn(lambda VN: VN.ID == 11)
        except Exception:
            vn = False
        results.put_nowait(vn)
        client.stop()

    await client.connect()

    assert not results.empty()
    result = results.get_nowait()
    assert isinstance(result, t.MutableSequence)
    assert all([isinstance(i, azaka.objects.VN) for i in result])
