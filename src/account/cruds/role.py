"""
Create, Read, Update, Delete operations for the role model
"""

from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from src.account.models import Role
from src.account.schemas import RoleCreate


async def get_roles(session: AsyncSession) -> list[Role]:
    """
    Get all roles
    :param session: session to use for DB
    :return: list of roles
    :rtype list[Role]
    """
    queue = select(Role).order_by(Role.id)
    result: Result = await session.execute(queue)
    roles = result.scalars().all()
    return list(roles)


async def get_role(session: AsyncSession, role_id: int) -> Role | None:
    """
    Get role by id
    :param session: session to use for DB
    :param role_id: ID of the role
    :type role_id: int
    :return: Role by id or None
    :rtype Role | None
    """
    return await session.get(Role, role_id)


async def create_role(session: AsyncSession, role_in: RoleCreate) -> Role:
    """
    Create role
    :param session: session to use for DB
    :param role_in: role data to create
    :type role_in: RoleCreate
    :return: created role
    :rtype Role
    """
    role = Role(**role_in.dict())
    queue = select(Role).where(Role.name == role.name)
    result: Result = await session.execute(queue)
    existing_role = result.scalars().first()
    if existing_role:
        return existing_role
    session.add(role)
    await session.commit()

    return role
