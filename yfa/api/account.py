import uuid
from typing import List
from fastapi import APIRouter

import yfa.controllers.account as account_controller
from yfa.models.account import Account, AccountBase

router = APIRouter()


@router.get("/v1")
async def get_many() -> List[Account]:
    return await account_controller.get_all()


@router.get("/{id}/v1")
async def get_single(id: uuid.UUID):
    return await account_controller.get_single(id=id)


@router.post("/v1")
async def create(account: AccountBase):
    return await account_controller.create(account=account)


@router.put("/{id}/v1")
async def update(id: uuid.UUID, account: AccountBase):
    return await account_controller.update(
        id=id,
        account=account
    )


@router.delete("/{id}/v1")
async def delete(id: uuid.UUID):
    return await account_controller.delete(id=id)
