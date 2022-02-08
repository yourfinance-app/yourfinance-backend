import sqlalchemy.ext.asyncio as sa_io

import yfa
from yfa.config import get_sqlalchemy_user_url
from yfa.database.utils import (database_exists, create_database)


async def create_user_database(db_name: str):
    engine = sa_io.create_async_engine(
        get_sqlalchemy_user_url(db_name=db_name))
    if not await database_exists(engine.url):
        await create_database(engine.url)

    print("Created Database Exists: ", await database_exists(engine.url))

    # Lets build an up-to-date db
    # https://alembic.sqlalchemy.org/en/latest/cookbook.html#building-an-up-to-date-database-from-scratch
    from yfa.database import user_registry
    async with engine.begin() as conn:
        await conn.run_sync(user_registry.metadata.create_all)

    # Update Alembic's stamp
    import os
    from alembic.config import Config
    from alembic import command

    dirname = os.path.dirname(yfa.__file__)
    # ini_section refers to alembic main section within ini file
    alembic_cfg = Config(os.path.join(
        dirname, "alembic.ini"), ini_section="user")
    alembic_cfg.set_main_option("DB_NAME", db_name)
    command.stamp(alembic_cfg, "head")
