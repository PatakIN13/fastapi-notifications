"""
Create, Read, Update, Delete operations for the account model
"""

from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from src.account.models import Account
from src.account.schemas import AccountCreate
from src.account.utils import generate_api_key


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


async def get_account(
    session: AsyncSession,
    account_id: int,
) -> Account | None:
    """
    Get account by id
    :param session: session to use for DB
    :param account_id: ID of the account
    :type account_id: int
    :return: Account by id or None
    :rtype Account | None
    """
    return await session.get(Account, account_id)


async def create_account(
    session: AsyncSession,
    account_in: AccountCreate,
) -> Account:
    """
    Create account
    :param session: session to use for DB
    :param account_in: account data to create
    :type account_in: AccountCreate
    :return: created account
    :rtype Account
    """
    api_key = generate_api_key()
    account = Account(**account_in.dict(), api_key=api_key)
    session.add(account)
    await session.commit()

    return account


async def get_account_by_api_key(
    session: AsyncSession,
    api_key: str,
) -> Account | None:
    """
    Get account by API key
    :param session: session to use for DB
    :param api_key: API key of the account
    :type api_key: str
    :return: Account by API key or None
    :rtype Account | None
    """
    account = select(Account).where(Account.api_key == api_key)
    result: Result = await session.execute(account)
    return result.scalars().first()


async def update_role_account(
    session: AsyncSession,
    account: Account,
    role_id: int,
) -> Account | None:
    """
    Update role account
    :param session: session to use for DB
    :param account: account to update
    :type account: Account
    :param role_id: ID of the role
    :type role_id: int
    :return: updated account
    :rtype Account | None if role not found
    """
    setattr(account, "role_id", role_id)

    await session.commit()
    return account
