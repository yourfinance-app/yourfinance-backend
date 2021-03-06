import uuid
import datetime
from sqlmodel import SQLModel, Field

from yfa.database import user_registry


class AccountBase(SQLModel, registry=user_registry):
    title: str
    description: str = None
    balance: float = 0
    currency: str = Field(max_length=5)
    account_group: uuid.UUID = Field(foreign_key="account_group.id")
    cc_settlement_date: datetime.date = None
    cc_payment_date: datetime.date = None


class Account(AccountBase, table=True):
    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        primary_key=True,
    )
