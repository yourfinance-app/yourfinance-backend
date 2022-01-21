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
