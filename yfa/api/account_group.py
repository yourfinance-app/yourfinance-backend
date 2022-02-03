import uuid
from typing import List
from fastapi import APIRouter

import yfa.controllers.account_groups as account_group_controllers
from yfa.models.account_group import AccountGroup, AccountGroupBase

router = APIRouter()


@router.get("/v1")
async def get_many() -> List[AccountGroup]:
    return await account_group_controllers.get_all()


@router.get("/{id}/v1")
async def get_single(id: uuid.UUID):
    return await account_group_controllers.get(id=id)


@router.post("/v1")
async def create(account_group: AccountGroupBase):
    return await account_group_controllers.create(account_group=account_group)


@router.put("/{id}/v1")
async def update(id: uuid.UUID, account_group: AccountGroupBase):
    return await account_group_controllers.update(
        id=id,
        account_group=account_group
    )


@router.delete("/{id}/v1")
async def delete(id: uuid.UUID):
    return await account_group_controllers.delete(id=id)
