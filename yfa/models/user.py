import uuid
from sqlmodel import SQLModel, Field
from pydantic import EmailStr


class UserEmailLoginInput(SQLModel):
    email_id: EmailStr
    pwd: str


class UserBase(SQLModel):
    first_name: str
    last_name: str = None
    country: str
    email_id: EmailStr = None


class UserEmailSignupInput(UserBase):
    email_id: EmailStr
    pwd: str


class User(UserBase, table=True):
    __tablename__ = "yfa_user"

    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        primary_key=True, nullable=False,
    )
    password_hash: str = None
    db_name: str

    def get_user_base(self) -> UserBase:
        return UserBase(**self.__dict__).__dict__
