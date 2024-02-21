"""Account router module."""

from fastapi import APIRouter, HTTPException, status, Depends

from src.account import utils
from src.account.repository.account import AccountRepository
from src.account.repository.role import RoleRepository
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


async def check_role_exists(role_id: int):
    """Check if role exists."""
    if await RoleRepository.find_by_id(model_id=role_id) is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Role not found"
        )


@router_admin.get(
    "/all/",
    response_model=list[Account],
)
async def get_accounts():
    """Get all accounts."""
    return await AccountRepository.get_all()


@router_admin.get("/id/", response_model=Account)
async def get_account_by_id(account_id: int):
    """Get account by id."""
    existing_account = await AccountRepository.find_by_id(model_id=account_id)
    if existing_account is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Account not found"
        )
    return existing_account


@router_admin.post("/api_key/", response_model=Account)
async def get_account_bu_api_key(api_key: str):
    """Find account by API key."""
    existing_account = await AccountRepository.find_one_or_none(api_key=api_key)
    if existing_account is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Account not found"
        )
    return existing_account


@router_admin.post("/create/", response_model=Account)
async def create_account(account_in: AccountCreate):
    """Create account."""

    await check_role_exists(role_id=account_in.role_id)

    key = utils.generate_api_key()
    account = await AccountRepository.create(
        api_key=key,
        name=account_in.name,
        role_id=account_in.role_id,
    )
    return await AccountRepository.find_by_id(model_id=account)


@router_admin.put("/update/", response_model=Account)
async def update_role_account(account_id: int, role_id: int):
    """Update role account."""
    if await AccountRepository.find_by_id(model_id=account_id) is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Account not found"
        )
    await check_role_exists(role_id=role_id)
    account = await AccountRepository.update_data(model_id=account_id, role_id=role_id)
    return await AccountRepository.find_by_id(model_id=account)
