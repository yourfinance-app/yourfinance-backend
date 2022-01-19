from sqlmodel import SQLModel, Field


class UserBase(SQLModel):
    first_name: str
    last_name: str = None
    country: str
    email_id: str = None
    password_hash: str = None
    password_salt: str = None
    db_name: str = None
    db_pwd: str = None


class User(UserBase, table=True):
    id: int = Field(default=None, primary_key=True)
