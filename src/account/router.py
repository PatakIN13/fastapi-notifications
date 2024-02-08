"""Account router module."""

from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import db_helper
from src.account import crud
from src.account.schemas import Account, AccountCreate

router = APIRouter(
    prefix="/account",
    tags=["Account"],
)


@router.get("/", response_model=list[Account])
async def get_accounts(
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    """Get all accounts."""
    return await crud.get_accounts(session=session)


@router.post("/", response_model=Account)
async def create_account(
    account_in: AccountCreate,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    """Create account."""
    return await crud.create_account(session=session, account_in=account_in)


@router.get("/{account_id}/", response_model=Account)
async def get_account(
    account_id: int,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    """Get account by id."""
    account = await crud.get_account(session=session, account_id=account_id)
    if account is not None:
        return account

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Account not found"
    )
