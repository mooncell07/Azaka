from __future__ import annotations

import asyncio
import typing as t

import azaka
import pytest


@pytest.mark.asyncio
async def test_vn() -> None:
    client = azaka.Client()
    results: asyncio.Queue[
        t.Union[None, t.Literal[False], t.List[azaka.objects.VN]]
    ] = asyncio.Queue()

    @client.register
    async def inner(ctx: azaka.Context) -> None:
        vn: t.Union[None, t.Literal[False], t.List[azaka.objects.VN]] = False
        try:
            vn = await ctx.get_vn(lambda VN: VN.ID == 11)
        finally:
            results.put_nowait(vn)
            client.stop()

    await client.connect()

    assert not results.empty()
    result = results.get_nowait()
    assert isinstance(result, t.MutableSequence)
    assert all([isinstance(i, azaka.objects.VN) for i in result])
