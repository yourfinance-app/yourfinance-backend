import uuid
from typing import List
from sqlmodel import select

import yfa
from yfa.exceptions import NotFound
from yfa.models.account_group import AccountGroupBase, AccountGroup


async def get_single(id: uuid.UUID) -> AccountGroup:
    return await yfa.db.get(AccountGroup, id)


async def get_all() -> List[AccountGroup]:
    result = await yfa.db.scalars(select(AccountGroup))
    return result.all()


async def create(account_group: AccountGroupBase) -> AccountGroup:
    account_group = AccountGroup(**account_group.__dict__)
    yfa.db.add(account_group)

    return account_group


async def update(id: uuid.UUID, account_group: AccountGroupBase) -> AccountGroup:
    _account_group = await get_single(id)
    if not _account_group:
        raise NotFound()
    _account_group.title = account_group.title
    yfa.db.add(_account_group)
    await yfa.db.flush()
    await yfa.db.refresh(_account_group)

    return _account_group


async def delete(id: uuid.UUID) -> bool:
    account_group = await get_single(id)
    if not account_group:
        raise NotFound()
    await yfa.db.delete(account_group)

    return True
