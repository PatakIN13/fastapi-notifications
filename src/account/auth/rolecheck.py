"""Role check privilege."""

from fastapi import HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import db_helper
from src.account.auth.apikey import auth_api_key
from src.account.schemas import Account
from src.account.cruds.role import get_role


async def auth_role_privilege(
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
    account: Account = Depends(auth_api_key),
) -> Account | HTTPException:
    """Check if the account has enough privileges."""
    unauthorized_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Not enough permissions",
    )
    if account.role_id == -1:
        return account
    role = await get_role(session=session, role_id=account.role_id)
    if role is None or role.name != "admin":
        raise unauthorized_exception

    return account
