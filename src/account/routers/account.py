"""Account router module."""

from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import db_helper
from src.account.cruds import account as crud
from src.account.schemas import Account, AccountCreate
from src.account.auth import auth_api_key, auth_role_privilege

router = APIRouter(
    prefix="/account",
    tags=["Account"],
)


@router.get("/me/", response_model=Account)
async def get_account(account: Account = Depends(auth_api_key)):
    """Get account by id."""
    return account


router_admin = APIRouter(
    prefix="/account",
    tags=["Account"],
    dependencies=[Depends(auth_role_privilege)],
)


@router_admin.get(
    "/",
    response_model=list[Account],
)
async def get_accounts(
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    """Get all accounts."""
    return await crud.get_accounts(session=session)


@router_admin.post("/", response_model=Account)
async def create_account(
    account_in: AccountCreate,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    """Create account."""
    return await crud.create_account(session=session, account_in=account_in)


@router_admin.post("/api_key/", response_model=Account)
async def get_account_by_api_key(
    account_api_key: str,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    """Get account by API key."""
    account_find = await crud.get_account_by_api_key(
        session=session, api_key=account_api_key
    )
    if account_find is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Account not found"
        )
    return account_find
