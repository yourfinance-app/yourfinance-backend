import sqlalchemy.ext.asyncio as sa
from sqlmodel import SQLModel

from yfa.config import get_sqlalchemy_core_url


async def make_core_db():
    engine = sa.create_async_engine(get_sqlalchemy_core_url())
    metadata = SQLModel.metadata

    async with engine.begin() as conn:
        await conn.run_sync(metadata.drop_all)
        await conn.run_sync(metadata.create_all)

    print("CoreDB Reset")
