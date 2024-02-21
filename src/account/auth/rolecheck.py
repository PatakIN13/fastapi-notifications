"""Role check privilege."""

from fastapi import HTTPException, status, Depends

from src.account.auth.apikey import auth_api_key
from src.account.schemas import Account
from src.account.repository.role import RoleRepository


async def auth_role_privilege(
    account: Account = Depends(auth_api_key),
) -> Account | HTTPException:
    """Check if the account has enough privileges."""
    unauthorized_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Not enough permissions",
    )
    if account.role_id == -1:
        return account
    role = await RoleRepository.find_by_id(model_id=account.role_id)
    if role is None or role.name != "admin":
        raise unauthorized_exception

    return account
