from fastapi import FastAPI, Request, Response
from starlette.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

import yfa


class YFAException(Exception):
    http_status_code = 500
    message = "Unknown Error"
    error_code = "UNKNOWN_ERROR"
    data = dict()

    def as_dict(self):
        return dict(
            http_status_code=self.http_status_code,
            message=self.message, error_code=self.error_code
        )


class YFAExceptionMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: FastAPI):
        self.app = app

    async def dispatch_func(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        yfa.request.set(request)

        r = {
            "data": None,
            "status": "OK",
            "errors": None
        }
        status_code = 200
        try:
            response = await call_next(request)
        except YFAException as e:  # noqa
            r["status"] = "FAILED"
            r["errors"] = [
                e.as_dict()
            ]
            status_code = e.http_status_code

        if isinstance(response, Response):
            return response

        r["data"] = response
        response = JSONResponse(r)
        response.status_code = status_code
        return response


class NotFound(YFAException):
    http_status_code = 404
    message = "Requested Entity Not Found"
    error_code = "NOT_FOUND"


class InvalidCountry(YFAException):
    http_status_code = 400
    message = "Invalid Country"
    error_code = "INVALID_COUNTRY"


class InvalidPassword(YFAException):
    http_status_code = 400
    message = "Invalid Password"
    error_code = "INVALID_PASSWORD"

    def __init__(self, result: dict) -> None:
        self.data = result
