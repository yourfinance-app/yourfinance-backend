from sqlmodel import select

import yfa
from yfa.models import UserEmailLoginInput, User
from yfa.exceptions import NotFound


async def email_login(input: UserEmailLoginInput):
    session = yfa.session.get()
    stmt = select(User).filter_by(email_id=input.email_id).limit(1)
    user = next(await session.execute(stmt), None)

    if not user:
        raise NotFound()
    return str(input)
