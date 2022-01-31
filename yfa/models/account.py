from sqlmodel import SQLModel, Field

from yfa.database import user_registry


class AccountBase(SQLModel, registry=user_registry):
    name: str


class Account(AccountBase, table=True):
    id: int = Field(default=None, primary_key=True)
