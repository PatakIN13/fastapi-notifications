"""
This file contains the authentication logic for the API.
"""

from fastapi.security.api_key import APIKeyHeader
from fastapi import Security, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import db_helper
from src.account.crud import get_account_by_api_key


api_key_header = APIKeyHeader(name="X-API-KEY", auto_error=False)


async def check_api_key(
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
    api_key: str = Security(api_key_header),
):
    """
    Check the API key
    :param session: session to use for DB
    :type session: AsyncSession
    :param api_key: api key to check
    :type api_key: str
    :return: Account if the API key is valid, raise an exception otherwise
    :rtype Account | raise HTTPException
    """
    unauthorized_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid API Key",
        headers={"WWW-Authenticate": "API Key"},
    )
    account = await get_account_by_api_key(session=session, api_key=api_key)
    if account is None:
        raise unauthorized_exception
    return account
