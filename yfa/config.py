import logging  # noqa: F401
from pydantic import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    LOG_LEVEL: str = "DEBUG"

    PGSQL_HOST: str
    PGSQL_PORT: int
    PGSQL_DB_CORE: str
    PGSQL_USER: str
    PGSQL_PWD: str

    REDIS_PORT: int
    REDIS_HOST: str
    REDIS_USER: str = None
    REDIS_PWD: str = None
    REDIS_USE_SENTINEL: bool = False


config = Settings()


def get_sqlalchemu_url(driver, user, pwd, host, port, db_name):
    """
    driver://user:pass@localhost:port/dbname
    """
    return f"{driver}://{user}:{pwd}@{host}:{port}/{db_name}"


def get_sqlalchemy_core_url():
    url = get_sqlalchemu_url(
        driver="postgresql+asyncpg",
        user=config.PGSQL_USER, pwd=config.PGSQL_PWD,
        host=config.PGSQL_HOST, port=config.PGSQL_PORT,
        db_name=config.PGSQL_DB_CORE
    )

    return url


def get_sqlalchemy_user_url():
    return None
