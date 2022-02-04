import uuid
from typing import List
from sqlmodel import select

import yfa
from yfa.exceptions import NotFound
from yfa.models.account_group import AccountGroupBase, AccountGroup


async def get_single(id: uuid.UUID) -> AccountGroup:
    return await yfa.locals.db.get(AccountGroup, id)


async def get_all() -> List[AccountGroup]:
    result = await yfa.locals.db.scalars(select(AccountGroup))
    return result.all()


async def create(account_group: AccountGroupBase) -> AccountGroup:
    locals = yfa.locals

    account_group = AccountGroup(**account_group.__dict__)
    locals.db.add(account_group)

    return account_group


async def update(id: uuid.UUID, account_group: AccountGroupBase) -> AccountGroup:
    locals = yfa.locals

    _account_group = await get_single(id)
    if not _account_group:
        raise NotFound()
    _account_group.title = account_group.title
    locals.db.add(_account_group)
    await locals.db.flush()
    await locals.db.refresh(_account_group)

    return _account_group


async def delete(id: uuid.UUID) -> bool:
    locals = yfa.locals

    account_group = await get_single(id)
    if not account_group:
        raise NotFound()
    await locals.db.delete(account_group)

    return True
