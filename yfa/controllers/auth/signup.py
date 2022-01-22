from sqlmodel import select, func
from pydantic import BaseModel

import yfa
from yfa.models import UserEmailSignupInput, User
from yfa.utils.data import validate_country, validate_password, generate_random


class IdentityProviderSignup(BaseModel):
    pass


async def email_signup(data: UserEmailSignupInput):

    # TODO: Validate Email
    # TODO: Validate Email OTP
    validate_password(data.pwd, throw=True)
    data.country = validate_country(data.country)
    await validate_unique_email(data.email_id)

    user = User(
        first_name=data.first_name, last_name=data.last_name, country=data.country,
        email_id=data.email_id,
    )
    user.db_name = f"yfa_{generate_random(15)}"
    # TODO: Check Email used in ID-Provided User
    # TODO: Create new DB

    # Make the new User and save it in DB

    print(r)
    return None


async def identity_provider_signup(data: IdentityProviderSignup):
    pass


async def validate_unique_email(email_id: str):
    db = yfa.session.get()
    r = await db.scalar(select([func.count()]).select_from(User).filter_by(email_id=email_id))
    if r > 0:
        # TODO: Update Exception Class
        raise Exception("Duplicate Email")
