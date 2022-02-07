import uuid
from sqlmodel import SQLModel, Field, Column, String
from yfa.database import user_registry


class AccountGroupBase(SQLModel, registry=user_registry):
    title: str = Field(sa_column=Column("title", String(50), unique=True))


class AccountGroup(AccountGroupBase, table=True):
    __tablename__ = "account_group"
    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        primary_key=True,
    )
