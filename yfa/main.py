from fastapi import FastAPI, Request, Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import JSONResponse

import yfa
from .exceptions import YFAException, UnknownError
from .config import config
from .utils import RedisClient
from .database import DatabaseMiddleware
from .models import *  # noqa
from .api import router as api_router
from .controllers.auth.jwt import decode_token


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
    app.add_middleware(YFAMiddleware)
    app.state.config = config

    app.include_router(api_router)

    @app.get("/")
    def root():
        return {"message": "Hello!"}

    return app


class YFAMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: FastAPI):
        self.app = app

    async def dispatch_func(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        yfa.locals.init_request(request=request)
        r = {
            "data": None,
            "status": "OK",
            "errors": None
        }
        status_code = 200
        response = None
        try:
            if "Authorization" in request.headers:
                yfa.locals.current_user = decode_token(request.headers.get(
                    "Authorization").split(" ")[1])
            response = await call_next(request)
        except YFAException as e:  # noqa
            r["status"] = "FAILED"
            r["errors"] = [
                e.as_dict()
            ]
            status_code = e.http_status_code
        except Exception as e:
            status_code = 500
            r["status"] = "FAILED"
            r["errors"] = [
                UnknownError(e).as_dict()
            ]

        background_tasks = yfa.locals.background_tasks
        yfa.locals.release_local()

        if isinstance(response, Response):
            response.background = background_tasks
            return response

        r["data"] = response
        response = JSONResponse(r, background=background_tasks)
        response.status_code = status_code
        return response


application = get_app()
