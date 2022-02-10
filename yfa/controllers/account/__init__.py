import uuid
from typing import List
from sqlmodel import select

import yfa
from yfa.exceptions import NotFound
from yfa.models.account import AccountBase, Account


async def get_single(id: uuid.UUID) -> Account:
    return await yfa.db.get(Account, id)


async def get_all() -> List[Account]:
    result = await yfa.db.scalars(select(Account))
    return result.all()


async def create(account: AccountBase) -> Account:
    account = Account(**account.__dict__)
    yfa.db.add(account)

    return account


async def update(id: uuid.UUID, account: AccountBase) -> Account:
    _account = await get_single(id)
    if not _account:
        raise NotFound()
    _account.title = account.title
    yfa.db.add(_account)
    await yfa.db.flush()
    await yfa.db.refresh(_account)

    return _account


async def delete(id: uuid.UUID) -> bool:
    account = await get_single(id)
    if not account:
        raise NotFound()
    await yfa.db.delete(account)

    return True
