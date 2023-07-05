import os

import pytest
from dotenv import load_dotenv

from azaka import Client
from azaka.exceptions import InvalidAuthTokenError
from azaka.models import AuthInfo, Stats, User


VALID_NAME = "Azaka"
INVALID_NAME = "NoUserWithThisNameExists"


@pytest.mark.asyncio
async def test_get_stats() -> None:
    client = Client()

    stats = await client.get_stats()
    assert isinstance(stats, Stats)

    await client.close_cs()


@pytest.mark.asyncio
async def test_get_user() -> None:
    client = Client()

    users = await client.get_user(VALID_NAME)
    for u in users:
        assert isinstance(u, User)
        assert VALID_NAME == u.search_term
        assert u.FOUND == True

    users = await client.get_user(INVALID_NAME)
    for u in users:
        assert isinstance(u, User)
        assert INVALID_NAME == u.search_term
        assert u.FOUND == False

    await client.close_cs()


@pytest.mark.asyncio
async def test_get_auth_info() -> None:
    load_dotenv()
    client = Client(token=os.getenv("TOKEN"))
    info = await client.get_auth_info()
    assert isinstance(info, AuthInfo)

    client.token = "faketoken"
    with pytest.raises(InvalidAuthTokenError):
        await client.get_auth_info()

    client.token = None
    with pytest.raises(TypeError):
        await client.get_auth_info()

    await client.close_cs()


@pytest.mark.asyncio
async def test_get_schema() -> None:
    client = Client()

    schema = await client.get_schema()
    assert isinstance(schema, dict)

    await client.close_cs()
