from pydantic import BaseModel


class SignupInput(BaseModel):
    email_id: str
    first_name: str
    last_name: str
    country: str
    password: str


class IdentityProviderSignup(BaseModel):
    pass


async def signup(data: SignupInput):
    pass


async def identity_provider_signup(data: IdentityProviderSignup):
    pass
