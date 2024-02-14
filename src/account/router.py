"""Account router module."""

from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security.api_key import APIKey
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import db_helper
from src.account import crud
from src.account.schemas import Account, AccountCreate
from src.account.auth import check_api_key

router = APIRouter(
    prefix="/account",
    tags=["Account"],
)


@router.get(
    "/",
    response_model=list[Account],
)
async def get_accounts(
    account: APIKey = Depends(check_api_key),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    """Get all accounts."""
    return await crud.get_accounts(session=session)


@router.post("/", response_model=Account)
async def create_account(
    account_in: AccountCreate,
    account: APIKey = Depends(check_api_key),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    """Create account."""
    return await crud.create_account(session=session, account_in=account_in)


@router.get("/{account_id}/", response_model=Account)
async def get_account(
    account_id: int,
    account: APIKey = Depends(check_api_key),
):
    """Get account by id."""
    if account.id != account_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden",
        )
    return account
