import uuid
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
import sqlalchemy.ext.asyncio as sa_io
from sqlmodel import SQLModel

from yfa.config import get_sqlalchemy_core_url, get_sqlalchemy_user_url
from yfa.models import User


async def make_core_db():
    engine = sa_io.create_async_engine(get_sqlalchemy_core_url())
    metadata = SQLModel.metadata

    async with engine.begin() as conn:
        await conn.run_sync(metadata.drop_all)
        await conn.run_sync(metadata.create_all)

    print("CoreDB Reset")


async def drop_user(id: uuid.UUID):
    from . import database_exists, drop_database

    engine = sa_io.create_async_engine(get_sqlalchemy_core_url())
    stmt = sa.select(User).filter_by(id=id).limit(1)
    _sessionmaker = sessionmaker(engine, class_=sa_io.AsyncSession)

    async with _sessionmaker() as session:
        async with session.begin():
            user: User = await session.scalar(stmt)
            if not user:
                print(f"User with ID: {id} not found")
                return

            user_db_url = get_sqlalchemy_user_url(user.db_name)
            if await database_exists(user_db_url):
                await drop_database(user_db_url)

            await session.execute(sa.delete(User).filter_by(id=id))
            await session.commit()
