from sqlmodel import select

import yfa
from yfa.utils.data import verify_password
from yfa.models import UserEmailLoginInput, User
from yfa.exceptions import NotFound, InvalidPassword


async def email_login(input: UserEmailLoginInput):
    session = yfa.session.get()
    stmt = select(User).filter_by(email_id=input.email_id).limit(1)
    user: User = await session.scalar(stmt)

    if not user:
        raise NotFound()

    if not verify_password(pwd=input.pwd, hash=user.password_hash):
        raise InvalidPassword()

    return user.get_user_base()
