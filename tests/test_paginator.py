import pytest
from azaka import Node, Client, Paginator, select


MAX_RESULTS = 2
EXIT_AFTER = 3


@pytest.mark.asyncio
async def test_paginator() -> None:
    query = select("id", "title").frm("vn").where(Node("olang") == "en")
    response_counter = 0
    async with Client() as client:
        paginator = Paginator(
            client, query=query, max_results_per_page=MAX_RESULTS, exit_after=EXIT_AFTER
        )
        async for page in paginator:
            for vn in page.results:
                assert len(vn) == MAX_RESULTS

            response_counter += 1
        assert response_counter == EXIT_AFTER
