from fastapi import FastAPI

from .config import config
from .utils import RedisClient
from .database import DatabaseMiddleware
from .api import auth
from .models import *  # noqa


async def on_startup():
    await RedisClient.open_redis_client()


async def on_shutdown():
    await RedisClient.close_redis_client()


def get_app():
    app = FastAPI(
        on_startup=[on_startup],
        on_shutdown=[on_shutdown]
    )
    app.add_middleware(DatabaseMiddleware)
    app.state.config = config

    app.include_router(auth.router, prefix="/api/auth", tags=["auth"])

    @app.get("/")
    def root():
        return {"message": "Hello!"}

    return app


application = get_app()
