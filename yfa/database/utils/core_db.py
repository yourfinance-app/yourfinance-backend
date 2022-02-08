import uuid
import sqlalchemy as sa
import sqlalchemy.ext.asyncio as sa_io
from sqlmodel import SQLModel
from sqlalchemy import select

from yfa.config import get_sqlalchemy_core_url
from yfa.models import User


async def make_core_db():
    engine = sa_io.create_async_engine(get_sqlalchemy_core_url())
    metadata = SQLModel.metadata

    async with engine.begin() as conn:
        await conn.run_sync(metadata.drop_all)
        await conn.run_sync(metadata.create_all)

    print("CoreDB Reset")


async def drop_user(id: uuid.UUID):
    engine = sa_io.create_async_engine(get_sqlalchemy_core_url())
    stmt = sa.select(User).filter_by(id=id).limit(1)
    async with engine.begin() as conn:
        conn.