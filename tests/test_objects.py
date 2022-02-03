from __future__ import annotations

import asyncio
import typing as t

import azaka
import pytest
import itertools


@pytest.mark.asyncio
async def test_vn() -> None:
    client = azaka.Client()
    results: asyncio.Queue = asyncio.Queue()

    @client.register
    async def visualn(ctx: azaka.Context) -> None:
        vn: t.Union[None, t.Literal[False], t.List[azaka.objects.VN]] = False
        try:
            vn = await ctx.get_vn(lambda VN: VN.ID == 11)
        finally:
            results.put_nowait(vn)

    @client.register
    async def inter(ctx: azaka.Context) -> None:
        res: t.Union[t.Literal[False], t.List[t.Any]] = False
        with azaka.Interface(
            type=ctx.release, flags=(azaka.Flags.PRODUCERS,)
        ) as interface:
            interface.set_condition(lambda R: R.PLATFORMS == "win")
            interface.add_option(results=1)
        try:
            res = await client.get(interface=interface)  # type: ignore
        finally:
            results.put_nowait(res)

    @client.register
    async def dbstat(_: azaka.Context) -> None:
        db: t.Union[t.Literal[False], azaka.objects.DBStats] = False
        try:
            db = await client.dbstats()
        finally:
            results.put_nowait(db)
            client.stop()

    await client.connect()
    _assertions(results)


def _assertions(results) -> None:

    # Testing list of VN objects.
    assert not results.empty()
    vn_list = results.get_nowait()
    assert isinstance(vn_list, t.MutableSequence)
    assert all([isinstance(i, azaka.objects.VN) for i in vn_list])

    # Testing list of Release objects and the mini dataclasses they have.
    assert not results.empty()
    release_list = results.get_nowait()
    assert isinstance(release_list, t.MutableSequence)
    assert all([isinstance(i, azaka.objects.Release) for i in release_list])
    prods = itertools.chain(*[i.release_producers for i in release_list])
    assert isinstance(prods, t.MutableSequence)
    assert all([isinstance(p, azaka.objects.release.ReleaseProducer) for p in prods])

    # Testing DBStats object.
    assert not results.empty()
    dbs = results.get_nowait()
    assert isinstance(dbs, azaka.objects.DBStats)
