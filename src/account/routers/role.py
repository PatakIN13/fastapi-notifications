"""Role router module."""

from fastapi import APIRouter, HTTPException, status, Depends

from src.account.repository.role import RoleRepository
from src.account.schemas import Role, RoleCreate
from src.account.auth import auth_role_privilege

router = APIRouter(
    prefix="/role", tags=["Role"], dependencies=[Depends(auth_role_privilege)]
)


@router.get(
    "/all/",
    response_model=list[Role],
)
async def get_roles():
    """Get all roles."""
    return await RoleRepository.get_all()


@router.get("/id/", response_model=Role)
async def get_role_by_id(role_id: int):
    """Get role by id."""
    existing_role = await RoleRepository.find_by_id(model_id=role_id)
    if existing_role is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Role not found"
        )
    return existing_role


@router.post("/name/", response_model=Role)
async def get_role_by_name(name: str):
    """Get role by name."""
    existing_role = await RoleRepository.find_one_or_none(name=name)
    if existing_role is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Role not found"
        )
    return existing_role


@router.post("/create/", response_model=Role)
async def create_role(role_in: RoleCreate):
    """Create role."""
    if await RoleRepository.find_one_or_none(name=role_in.name) is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Role already exists"
        )
    role = await RoleRepository.create(**role_in.dict())
    return await RoleRepository.find_by_id(model_id=role)
