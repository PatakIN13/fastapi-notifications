"""Role router module."""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import db_helper
from src.account.cruds import role as crud
from src.account.schemas import Role, RoleCreate
from src.account.auth import check_admin

router = APIRouter(
    prefix="/role",
    tags=["Role"],
)


@router.get(
    "/",
    response_model=list[Role],
)
async def get_roles(
    admin: bool = Depends(check_admin),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    """Get all roles."""
    return await crud.get_roles(session=session)


@router.post("/", response_model=Role)
async def create_role(
    role_in: RoleCreate,
    admin: bool = Depends(check_admin),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    """Create role."""
    return await crud.create_role(session=session, role_in=role_in)