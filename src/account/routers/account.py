"""Account router module."""

from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import db_helper
from src.account.cruds import account as crud
from src.account.schemas import Account, AccountCreate
from src.account.auth import check_api_key, check_admin

router = APIRouter(
    prefix="/account",
    tags=["Account"],
)


@router.get(
    "/",
    response_model=list[Account],
)
async def get_accounts(
    admin: bool = Depends(check_admin),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    """Get all accounts."""
    return await crud.get_accounts(session=session)


@router.post("/", response_model=Account)
async def create_account(
    account_in: AccountCreate,
    admin: bool = Depends(check_admin),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    """Create account."""
    return await crud.create_account(session=session, account_in=account_in)


@router.get("/me/", response_model=Account)
async def get_account(
    account: Account = Depends(check_api_key),
):
    """Get account by id."""
    return account


@router.get("/api_key/", response_model=Account)
async def get_account_by_api_key(
    api_key: str,
    admin: bool = Depends(check_admin),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    """Get account by API key."""
    account = await crud.get_account_by_api_key(session=session, api_key=api_key)
    if account is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Account not found"
        )
    return account
