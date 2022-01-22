from fastapi import FastAPI
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

from sqlalchemy.orm import sessionmaker, registry
from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine, create_async_engine

import yfa
from yfa.config import get_sqlalchemy_core_url


class DatabaseMiddleware(BaseHTTPMiddleware):
    engines: dict[str, AsyncEngine] = dict()
    temporary_engines = []

    def __init__(self, app: FastAPI):
        self.app = app
        self.engines["main"] = create_async_engine(
            url=get_sqlalchemy_core_url(),
            future=True,
            echo=True,
        )

    async def dispatch_func(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        session_maker = sessionmaker(self.engines["main"], class_=AsyncSession)
        async with session_maker() as session:
            async with session.begin():
                yfa.session.set(session)
                response = await call_next(request)

        return response


user_registry = registry()
