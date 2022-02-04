from contextvars import Token, ContextVar
from starlette.background import BackgroundTasks
from starlette.requests import Request
from sqlalchemy.ext.asyncio import AsyncSession
from .config import config  # noqa: F401
from .models.user import UserJWTContent
from typing import Generic, TypeVar

try:
    VERSION = __import__("pkg_resources").get_distribution("dispatch").version
except Exception:
    VERSION = "unknown"

__version__ = VERSION

T = TypeVar("T")


class Locals:
    _request: ContextVar[Request] = ContextVar("request", default=None)
    _request_token: Token[Request]

    @property
    def request(self):
        return self._request.get()

    @request.setter
    def request(self, value: Request):
        self._request_token = self._request.set(value)
        return self._request_token

    @request.deleter
    def request(self):
        self._request.reset(self._request_token)
        self._request_token = None

    _db: ContextVar[AsyncSession] = ContextVar("db", default=None)
    _db_token: Token[AsyncSession]

    @property
    def db(self):
        return self._db.get()

    @db.setter
    def db(self, value: AsyncSession):
        self._db_token = self._db.set(value)
        return self._db_token

    @db.deleter
    def db(self):
        if not self._db_token:
            return None
        self._db.reset(self._db_token)
        self._db_token = None

    _background_tasks: ContextVar[BackgroundTasks] = ContextVar(
        "background_tasks", default=None)
    _background_tasks_token: Token[BackgroundTasks]

    @property
    def background_tasks(self):
        return self._background_tasks.get()

    @background_tasks.setter
    def background_tasks(self, value: BackgroundTasks):
        self._background_tasks_token = self._background_tasks.set(value)
        return self._background_tasks_token

    @background_tasks.deleter
    def background_tasks(self):
        if not self._background_tasks_token:
            return
        self._background_tasks.reset(self._background_tasks_token)
        self._background_tasks_token = None

    _current_user: ContextVar[UserJWTContent] = ContextVar(
        "current_user", default=None)
    _current_user_token: Token[UserJWTContent] = None

    @property
    def current_user(self):
        return self._current_user.get()

    @current_user.setter
    def current_user(self, value: UserJWTContent):
        self._current_user_token = self._current_user.set(value)
        return self._current_user_token

    @current_user.deleter
    def current_user(self):
        if not self._current_user_token:
            return
        self._current_user.reset(self._current_user_token)

    def get_local(self, name: str, type: Generic[T]) -> T:
        return getattr(name)

    def init_request(self, request: Request):
        self.request = request
        self.background_tasks = BackgroundTasks()

    def release_local(self):
        try:
            del self.request
            del self.background_tasks
            del self.db
            del self.current_user
        except BaseException:
            pass


locals = Locals()
request: Request
db: AsyncSession
background_tasks: BackgroundTasks
current_user: UserJWTContent


def __getattr__(name: str):
    global locals
    if name in ["request", "db", "background_tasks", "current_user"]:
        return getattr(locals, name)

    return globals()[name]
