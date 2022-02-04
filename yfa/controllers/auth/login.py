from sqlmodel import select

import yfa
from yfa.utils.data import verify_password
from yfa.models import UserEmailLoginInput, User, UserLoginResponse
from yfa.exceptions import NotFound, InvalidPassword


async def email_login(input: UserEmailLoginInput):
    locals = yfa.locals
    stmt = select(User).filter_by(email_id=input.email_id).limit(1)
    user: User = await locals.db.scalar(stmt)

    if not user:
        raise NotFound()

    if not verify_password(pwd=input.pwd, hash=user.password_hash):
        raise InvalidPassword()

    from .jwt import make_token
    jwt_token = make_token(user)

    return UserLoginResponse(
        **user.__dict__,
        jwt_token=jwt_token
    )
