from fastapi import FastAPI
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

from sqlalchemy.orm import sessionmaker, registry
from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine, create_async_engine

import yfa
from yfa.config import get_sqlalchemy_core_url, get_sqlalchemy_user_url


class DatabaseMiddleware(BaseHTTPMiddleware):
    engines: dict[str, AsyncEngine] = dict()
    temporary_engines = []
    echo = True

    def __init__(self, app: FastAPI):
        self.app = app
        self.engines["main"] = create_async_engine(
            url=get_sqlalchemy_core_url(),
            future=True,
            echo=self.echo,
        )

    def get_user_engine(self, db_name: str):
        if db_name in self.engines:
            return self.engines[db_name]
        else:
            self.engines[db_name] = create_async_engine(
                url=get_sqlalchemy_user_url(db_name=db_name),
                future=True, echo=self.echo
            )
            return self.engines[db_name]

    async def dispatch_func(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        if yfa.locals.current_user:
            engine = self.get_user_engine(yfa.locals.current_user.db_name)
        else:
            engine = self.engines["main"]

        session_maker = sessionmaker(engine, class_=AsyncSession)
        async with session_maker() as session:
            async with session.begin():
                yfa.locals.db = session
                response = await call_next(request)
                await session.commit()
                del yfa.locals.db

        return response


user_registry = registry()
