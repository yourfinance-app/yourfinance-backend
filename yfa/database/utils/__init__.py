import sqlalchemy as sa
from sqlalchemy.engine.url import make_url, URL
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
from sqlalchemy.exc import OperationalError, ProgrammingError
from sqlalchemy.orm.session import object_session
from sqlalchemy.orm.exc import UnmappedInstanceError

import yfa
from yfa.config import get_sqlalchemy_user_url


async def create_user_database(db_name: str):
    engine = create_async_engine(get_sqlalchemy_user_url(db_name=db_name))
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


async def database_exists(url: str) -> bool:
    """Check if a database exists.

    :param url: A SQLAlchemy engine URL.

    Performs backend-specific testing to quickly determine if a database
    exists on the server. ::

        database_exists('postgresql://postgres@localhost/name')  #=> False
        create_database('postgresql://postgres@localhost/name')
        database_exists('postgresql://postgres@localhost/name')  #=> True

    Supports checking against a constructed URL as well. ::

        engine = create_async_engine('postgresql://postgres@localhost/name')
        database_exists(engine.url)  #=> False
        create_database(engine.url)
        database_exists(engine.url)  #=> True

    """

    url: URL = make_url(url)
    database = url.database
    dialect_name = url.get_dialect().name
    engine = None
    try:
        if dialect_name == 'postgresql':
            text = sa.text(
                "SELECT 1 FROM pg_database WHERE datname='%s'" % database)
            for db in (database, 'postgres', 'template1', 'template0', None):
                url = _set_url_database(url, database=db)
                engine = create_async_engine(url)
                try:
                    return bool(await _get_scalar_result(engine, text))
                # except (ProgrammingError, OperationalError):
                except Exception as e:  # noqa
                    pass
            return False

        elif dialect_name == 'mysql':
            url = _set_url_database(url, database=None)
            engine = create_async_engine(url)
            text = sa.text("SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA "
                           "WHERE SCHEMA_NAME = '%s'" % database)
            return bool(await _get_scalar_result(engine, text))

        elif dialect_name == 'sqlite':
            url = _set_url_database(url, database=None)
            engine = create_async_engine(url)
            if database:
                return database == ':memory:' or _sqlite_file_exists(database)
            else:
                # The default SQLAlchemy database is in memory, and :memory is
                # not required, thus we should support that use case.
                return True
        else:
            text = sa.text('SELECT 1')
            try:
                engine = create_async_engine(url)
                return bool(await _get_scalar_result(engine, text))
            except (ProgrammingError, OperationalError):
                return False
    finally:
        if engine:
            await engine.dispose()


async def create_database(url: URL | str, encoding='utf8', template=None):
    """Issue the appropriate CREATE DATABASE statement.

    :param url: A SQLAlchemy engine URL.
    :param encoding: The encoding to create the database as.
    :param template:
        The name of the template from which to create the new database. At the
        moment only supported by PostgreSQL driver.

    To create a database, you can pass a simple URL that would have
    been passed to ``create_async_engine``. ::

        create_database('postgresql://postgres@localhost/name')

    You may also pass the url from an existing engine. ::

        create_database(engine.url)

    Has full support for mysql, postgres, and sqlite. In theory,
    other database engines should be supported.
    """

    url = make_url(url)
    database = url.database
    dialect_name = url.get_dialect().name
    dialect_driver = url.get_dialect().driver

    if dialect_name == 'postgresql':
        url = _set_url_database(url, database="postgres")
    elif dialect_name == 'mssql':
        url = _set_url_database(url, database="master")
    elif not dialect_name == 'sqlite':
        url = _set_url_database(url, database=None)

    if (dialect_name == 'mssql' and dialect_driver in {'pymssql', 'pyodbc'}) \
            or (dialect_name == 'postgresql' and dialect_driver in {
            'asyncpg', 'pg8000', 'psycopg2', 'psycopg2cffi'}):
        engine = create_async_engine(url, isolation_level='AUTOCOMMIT')
    else:
        engine = create_async_engine(url)

    if dialect_name == 'postgresql':
        if not template:
            template = 'template1'

        text = sa.text("CREATE DATABASE {0} ENCODING '{1}' TEMPLATE {2}".format(
            quote(engine.sync_engine, database),
            encoding,
            quote(engine.sync_engine, template)
        ))

        async with engine.connect() as connection:
            await connection.execute(text)

    elif dialect_name == 'mysql':
        text = sa.text("CREATE DATABASE {0} CHARACTER SET = '{1}'".format(
            quote(engine.sync_engine, database),
            encoding
        ))
        async with engine.connect() as connection:
            await connection.execute(text)

    elif dialect_name == 'sqlite' and database != ':memory:':
        if database:
            async with engine.connect() as connection:
                await connection.execute(sa.text("CREATE TABLE DB(id int);"))
                await connection.execute(sa.text("DROP TABLE DB;"))

    else:
        text = sa.text('CREATE DATABASE {0}'.format(quote(engine.sync_engine, database)))
        async with engine.connect() as connection:
            await connection.execute(text)

    await engine.dispose()


def _set_url_database(url: sa.engine.url.URL, database):
    """Set the database of an engine URL.

    :param url: A SQLAlchemy engine URL.
    :param database: New database to set.

    """
    if hasattr(sa.engine, 'URL'):
        ret = sa.engine.URL.create(
            drivername=url.drivername,
            username=url.username,
            password=url.password,
            host=url.host,
            port=url.port,
            database=database,
            query=url.query
        )
    else:  # SQLAlchemy <1.4
        url.database = database
        ret = url
    assert ret.database == database, ret
    return ret


async def _get_scalar_result(engine: AsyncEngine, sql: str):
    async with engine.connect() as conn:
        return await conn.scalar(sql)


def _sqlite_file_exists(database):
    import os
    if not os.path.isfile(database) or os.path.getsize(database) < 100:
        return False

    with open(database, 'rb') as f:
        header = f.read(100)

    return header[:16] == b'SQLite format 3\x00'


def quote(mixed, ident):
    """
    Conditionally quote an identifier.
    ::


        from sqlalchemy_utils import quote


        engine = create_engine('sqlite:///:memory:')

        quote(engine, 'order')
        # '"order"'

        quote(engine, 'some_other_identifier')
        # 'some_other_identifier'


    :param mixed: SQLAlchemy Session / Connection / Engine / Dialect object.
    :param ident: identifier to conditionally quote
    """
    from sqlalchemy.engine.interfaces import Dialect

    if isinstance(mixed, Dialect):
        dialect = mixed
    else:
        dialect = get_bind(mixed).dialect
    return dialect.preparer(dialect).quote(ident)


def get_bind(obj):
    """
    Return the bind for given SQLAlchemy Engine / Connection / declarative
    model object.

    :param obj: SQLAlchemy Engine / Connection / declarative model object

    ::

        from sqlalchemy_utils import get_bind


        get_bind(session)  # Connection object

        get_bind(user)

    """
    if hasattr(obj, 'bind'):
        conn = obj.bind
    else:
        try:
            conn = object_session(obj).bind
        except UnmappedInstanceError:
            conn = obj

    if not hasattr(conn, 'execute'):
        raise TypeError(
            'This method accepts only Session, Engine, Connection and '
            'declarative model objects.'
        )
    return conn
