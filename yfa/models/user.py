from sqlmodel import SQLModel, Field
from pydantic import EmailStr


class UserEmailLoginInput(SQLModel):
    email_id: str
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
    id: int = Field(default=None, primary_key=True)
    password_hash: str = None
    db_name: str = None
