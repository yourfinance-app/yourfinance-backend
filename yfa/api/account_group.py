from fastapi import APIRouter
from typing import List

import yfa.controllers.account_groups as account_group_controllers
from yfa.models.account_group import AccountGroup, AccountGroupBase

router = APIRouter()


@router.get("/v1")
def get_many() -> List[AccountGroup]:
    return [1, 2]


@router.get("/{account_group}/v1")
def get_account_group(account_group: str):
    return account_group


@router.post("/v1")
def create(account_group: AccountGroupBase):
    return account_group_controllers.create(account_group=account_group)


@router.put("/{account_group}/v1")
def update(account_group: str, ):
    pass


@router.delete("/{account_group}/v1")
def delete(account_group: str):
    pass
