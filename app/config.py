from pydantic import BaseSettings


class Settings(BaseSettings):
    PGSQL_HOST: str
    PGSQL_PORT: int
    PGSQL_DB_MAIN: str
    PGSQL_USER: str
    PGSQL_PWD: str

    REDIS_PORT: int
    REDIS_HOST: str
    REDIS_USER: str = None
    REDIS_PWD: str = None
    REDIS_USE_SENTINEL: bool = False


settings = Settings()
