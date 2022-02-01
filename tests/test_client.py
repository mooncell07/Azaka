import asyncio
import typing as t

import azaka
import pytest


@pytest.mark.asyncio
async def test_connection() -> None:
    client = azaka.Client()
    old_state: asyncio.Queue = asyncio.Queue()

    @client.register
    async def inner(ctx: azaka.Context) -> None:
        await client.wait_until_connect()
        old_state.put_nowait(ctx.client.connected)
        client.stop()

    await client.connect()
    was_connected = old_state.get_nowait()
    assert old_state.empty()
    assert was_connected


@pytest.mark.asyncio
async def test_vn() -> None:
    client = azaka.Client()
    results: asyncio.Queue = asyncio.Queue()

    @client.register
    async def inner(ctx: azaka.Context) -> None:
        vn = await ctx.get_vn(lambda VN: VN.ID == 11)
        await results.put(vn)
        client.stop()

    await client.connect()

    result = await results.get()
    assert isinstance(result, t.MutableSequence)
    assert all([isinstance(i, azaka.objects.VN) for i in result])
