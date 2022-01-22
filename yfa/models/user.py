from sqlmodel import SQLModel, Field


class UserEmailLoginInput(SQLModel):
    email_id: str
    pwd: str


class UserBase(SQLModel):
    first_name: str
    last_name: str = None
    country: str
    email_id: str = None


class UserEmailSignupInput(UserBase):
    email_id: str
    pwd: str


class User(UserBase, table=True):
    id: int = Field(default=None, primary_key=True)
    db_pwd: str = None
    password_hash: str = None
    password_salt: str = None
    db_name: str = None
