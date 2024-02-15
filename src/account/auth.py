"""
This file contains the authentication logic for the API.
"""

from fastapi.security.api_key import APIKeyHeader
from fastapi import Security, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.settings import settings
from src.core.database import db_helper
from src.account.schemas import Account
from src.account.cruds.account import get_account_by_api_key
from src.account.cruds.role import get_role


api_key_header = APIKeyHeader(name="X-API-KEY", auto_error=False)


async def check_api_key(
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
    api_key: str = Security(api_key_header),
) -> Account:
    """
    Check the API key
    :param session: session to use for DB
    :type session: AsyncSession
    :param api_key: api key to check
    :type api_key: str
    :return: Account dict if the API key is valid, raise an exception otherwise
    :rtype Account | raise HTTPException
    """
    unauthorized_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid API Key",
        headers={"WWW-Authenticate": "API Key"},
    )
    if api_key == settings.secret_key:
        account = Account(
            id=0,
            role_id=0,
            name="admin",
            created_at=0,
            api_key=settings.secret_key,
        )
        return account
    account = await get_account_by_api_key(session=session, api_key=api_key)
    if account is None:
        raise unauthorized_exception
    return account


async def check_admin(
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
    account: Account = Depends(check_api_key),
) -> bool:
    """
    Check if the account is an admin
    :param account: account to check
    :type account: dict
    :return: True if the account is an admin, raise an exception otherwise
    :rtype True | raise HTTPException
    """
    if account.id == 0:
        return True

    role = await get_role(session=session, role_id=account.role_id)

    if role:
        if role.name == "admin":
            return True

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Forbidden",
    )
