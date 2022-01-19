from fastapi import APIRouter
from ..controllers.auth.signup import SignupInput, IdentityProviderSignup

router = APIRouter()


@router.get("/login/v1")
async def login():
    return {"status": "OK"}


@router.post("/signup/v1")
async def signup(input: SignupInput):
    return {"status": "OK"}


@router.post("/signup/{provider}/v1")
async def identity_provider_signup(input: IdentityProviderSignup):
    return {"status": "OK"}
