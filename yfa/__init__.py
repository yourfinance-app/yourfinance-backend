from contextvars import Context, ContextVar
from starlette.background import BackgroundTasks
from starlette.requests import Request
from sqlalchemy.ext.asyncio import AsyncSession
from .config import config  # noqa: F401
from .models.user import UserJWTContent

try:
    VERSION = __import__("pkg_resources").get_distribution("dispatch").version
except Exception:
    VERSION = "unknown"

__version__ = VERSION


class Locals:
    request: Request
    db: AsyncSession
    background_tasks: BackgroundTasks
    current_user: UserJWTContent = None


locals: ContextVar[Locals] = ContextVar("local", default=None)
