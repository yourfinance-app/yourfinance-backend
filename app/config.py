from pydantic import BaseSettings


class Settings(BaseSettings):
    PGSQL_HOST: str
    PGSQL_PORT: int
    PGSQL_DB_MAIN: str
    PGSQL_USER: str
    PGSQL_PWD: str


settings = Settings()
