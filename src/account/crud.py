"""
Create, Read, Update, Delete operations for the account model
"""

from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from src.account.models import Account

from src.account.schemas import AccountCreate


async def get_accounts(session: AsyncSession) -> list[Account]:
    """
    Get all accounts
    :param session: session to use for DB
    :return: list of accounts
    :rtype list[Account]
    """
    queue = select(Account).order_by(Account.id)
    result: Result = await session.execute(queue)
    accounts = result.scalars().all()
    return list(accounts)


async def get_account(session: AsyncSession, account_id: int) -> Account | None:
    """
    Get account by id
    :param session: session to use for DB
    :param account_id: ID of the account
    :type account_id: int
    :return: Account by id or None
    :rtype Account | None
    """
    return await session.get(Account, account_id)


async def create_account(session: AsyncSession, account_in: AccountCreate) -> Account:
    """
    Create account
    :param session: session to use for DB
    :param account_in: account data to create
    :type account_in: AccountCreate
    :return: created account
    :rtype Account
    """
    account = Account(**account_in.dict(), api_key="123")
    session.add(account)
    await session.commit()

    return account
