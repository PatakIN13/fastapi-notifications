"""Account repository module."""

from src.core.repository.base import BaseRepository
from src.account.models import Account


class AccountRepository(BaseRepository):
    """Account repository"""

    model = Account
