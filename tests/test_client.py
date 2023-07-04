import asyncio
import os
import re

import pytest
from dotenv import load_dotenv

import azaka
from azaka import AND, OR, Client, Node, Response, select

load_dotenv()
token = os.getenv("TOKEN")


req = (
    select(
        "titles.latin",
        "titles.official",
        "titles.main",
        "olang",
        "released",
        "languages",
        "platforms",
        "image.id",
        "image.url",
        "length_minutes",
    )
    .frm("vn")
    .where(Node("search") == "fate/stay night")
    .sort("rating")
)

req.set_flags(normalized_filters=True)


@pytest.mark.asyncio
async def test_execute():
    async with azaka.Client(token=token) as client:
        resp = await client.execute(req)
        assert isinstance(resp, Response)
        assert req._body["filters"] == resp.normalized_filters
        assert set(re.sub(r"\.[A-Za-z]+", "", req._body["fields"]).split(", ")) == set(
            resp.results[0]._fields
        )
