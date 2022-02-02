import uuid
from sqlmodel import SQLModel, Field
from yfa.database import user_registry


class AccountGroupBase(SQLModel, registry=user_registry):
    title: str


class AccountGroup(AccountGroupBase, table=True):
    __tablename__ = "account_group"
    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        primary_key=True,
    )
