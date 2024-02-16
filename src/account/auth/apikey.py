"""
This file contains the authentication logic for the API.
"""

from fastapi.security.api_key import APIKeyHeader
from fastapi import Security, HTTPException, status

from src.core.settings import settings
from src.core.database import db_helper
from src.account.schemas import Account
from src.account.cruds.account import get_account_by_api_key


api_key_header = APIKeyHeader(name="X-API-KEY", auto_error=False)


async def auth_api_key(
    api_key: str = Security(api_key_header),
) -> Account:
    """
    Check the APIKey
    :param api_key: key check for authentication
    :type api_key: str
    :return: Account dict if the API key is valid, raise an exception otherwise
    :rtype Account
    """
    unauthorized_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid API Key",
        headers={"WWW-Authenticate": "API Key"},
    )
    if api_key == settings.secret_key:
        return Account(
            id=0,
            role_id=-1,
            name="admin",
            created_at=0,
            api_key=settings.secret_key,
        )
    account = await get_account_by_api_key(
        session=db_helper.get_scoped_session(),
        api_key=api_key,
    )
    if account is None:
        raise unauthorized_exception

    return account
