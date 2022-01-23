import traceback
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
            message=self.message, error_code=self.error_code,
            data=self.data or {}
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
        response = None
        try:
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

        if isinstance(response, Response):
            return response

        r["data"] = response
        response = JSONResponse(r)
        response.status_code = status_code
        return response


class UnknownError(YFAException):
    def __init__(self, e: Exception):
        self.error_code = "UNKNOWN_ERROR"
        self.http_status_code = 500
        self.message = "Unknown Error"
        self.data = dict(
            traceback=''.join(traceback.format_tb(e.__traceback__)),
            exc=str(e)
        )


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


class DuplicateEntity(YFAException):
    http_status_code = 409
    message = "Duplicate Entity"
    error_code = "DUPLICATE_ENTITY"

    def __init__(self, entity_type: str, entity_value: str) -> None:
        self.data = dict(
            entity_type=entity_type,
            entity_value=entity_value
        )
