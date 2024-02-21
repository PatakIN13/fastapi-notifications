"""Role repository module."""

from src.core.repository.base import BaseRepository
from src.account.models import Role


class RoleRepository(BaseRepository):
    """Role repository"""

    model = Role
