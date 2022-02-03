import uuid

import yfa
from yfa.models.account_group import AccountGroupBase, AccountGroup
from typing import List


def get(id: uuid.UUID) -> AccountGroup:
    pass


def get_all() -> List[AccountGroup]:
    pass


def create(account_group: AccountGroupBase) -> AccountGroup:
    locals = yfa.locals.get()

    account_group = AccountGroup(**account_group.__dict__)
    locals.db.add(account_group)

    return account_group


def update(id: uuid.UUID, group: AccountGroupBase) -> AccountGroup:
    pass


def delete(id: uuid.UUID) -> bool:
    pass
