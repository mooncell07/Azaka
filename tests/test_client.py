import asyncio
import re

import pytest

from azaka import AND, OR, Client, Node, Response, select
from azaka.query import Query


async def execute_(req: Query) -> None:
    req.set_flags(normalized_filters=True)

    async with Client() as client:
        resp = await client.execute(req)
        fltrs = req._body["filters"] or None

        assert isinstance(resp, Response)
        assert fltrs == resp.normalized_filters
        assert set(re.sub(r"\.[A-Za-z]+", "", req._body["fields"]).split(", ")) == set(
            resp.results[0]._fields
        )


async def select_(q: Query) -> None:
    req1 = select().frm(q._route).where(q._body["filters"])
    req2 = (
        select(
            "titles.latin",
            "titles.official",
            " titles.main   ",
            "olang",
            "released",
            "lanGUages",
            "platforms",
            "image.id",
            "image.url",
            "length_minutes",
        )
        .frm(q._route)
        .where(q._body["filters"])
    )

    await execute_(req1)
    await execute_(req2)


async def frm_(q: Query) -> None:
    query = select()
    with pytest.raises(TypeError):
        await select_(query)

    query.frm("vn").where(q._body["filters"])
    await select_(query)


@pytest.mark.asyncio
async def test_where() -> None:  # TODO: add more filters.
    query = select().frm("vn").where()
    await frm_(query)

    query = select().frm("vn").where(Node("id") == "v2002")
    await frm_(query)

    query = select().frm("vn").where(["id", "=", "v2002"])
    await frm_(query)
