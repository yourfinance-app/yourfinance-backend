from fastapi import APIRouter
from yfa.controllers.auth import email_login, email_signup
from yfa.models import UserEmailLoginInput, UserEmailSignupInput
from ..controllers.auth.signup import IdentityProviderSignup

router = APIRouter()


@router.post("/login/v1")
async def login(input: UserEmailLoginInput):
    return await email_login(input)


@router.post("/signup/v1")
async def signup(input: UserEmailSignupInput):
    return await email_signup(input)


@router.post("/signup/{provider}/v1")
async def identity_provider_signup(input: IdentityProviderSignup):
    return None
