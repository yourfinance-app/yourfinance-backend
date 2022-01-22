from contextvars import ContextVar
from starlette.requests import Request
from sqlalchemy.ext.asyncio import AsyncSession

try:
    VERSION = __import__("pkg_resources").get_distribution("dispatch").version
except Exception:
    VERSION = "unknown"

__version__ = VERSION


request: ContextVar[Request] = ContextVar("starlette-request", default=None)
session: ContextVar[AsyncSession] = \
    ContextVar("active-db-session", default=None)
