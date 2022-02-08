from sqlmodel import select, func
from pydantic import BaseModel

import yfa
from yfa.exceptions import DuplicateEntity
from yfa.models import UserEmailSignupInput, User
from yfa.utils.data import validate_country, validate_password, generate_random, hash_password


class IdentityProviderSignup(BaseModel):
    pass


async def email_signup(data: UserEmailSignupInput):

    # TODO: Validate Email OTP
    # TODO: Check Email used in ID-Provided User

    data.country = validate_country(data.country)
    validate_password(data.pwd, throw=True)
    await validate_unique_email(data.email_id)

    user = User(
        first_name=data.first_name, last_name=data.last_name, country=data.country,
        email_id=data.email_id,
        password_hash=hash_password(pwd=data.pwd),
        db_name=f"yfa_{generate_random(15)}"
    )

    yfa.db.add(user)

    # Create a Background Task to make User DB
    from yfa.database.utils.user_db import create_user_database
    yfa.background_tasks.add_task(
        create_user_database, db_name=user.db_name)

    return user.get_user_base()


async def identity_provider_signup(data: IdentityProviderSignup):
    pass


async def validate_unique_email(email_id: str):
    r = await yfa.db.scalar(
        select([func.count()]).select_from(User).filter_by(email_id=email_id))
    if r > 0:
        raise DuplicateEntity(
            entity_type="email_id",
            entity_value=email_id
        )
