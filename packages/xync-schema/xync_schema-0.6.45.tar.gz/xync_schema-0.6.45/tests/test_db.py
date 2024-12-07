from os import getenv as env

import pytest
from dotenv import load_dotenv
from tortoise import connections
from tortoise.backends.asyncpg import AsyncpgDBClient
from x_model import init_db

from xync_schema import models
from xync_schema.models import Cur

load_dotenv()


@pytest.fixture
async def dbc() -> AsyncpgDBClient:
    await init_db(env("DB_URL"), models, True)
    cn: AsyncpgDBClient = connections.get("default")
    yield cn
    await cn.close()


async def test_init_db(dbc):
    assert isinstance(dbc, AsyncpgDBClient), "DB corrupt"


async def test_models(dbc):
    c = await Cur.all()
    assert isinstance(c, list), "No currencies"
