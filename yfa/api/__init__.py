from fastapi import APIRouter

from .auth import router as auth_router
from .account_group import router as account_group_router
from .account import router as account_router

router = APIRouter()
router.include_router(auth_router, prefix="/api/auth", tags=["auth"])
router.include_router(account_group_router,
                      prefix="/api/account_group", tags=["account_group"])
router.include_router(account_router,
                      prefix="/api/account", tags=["account"])
