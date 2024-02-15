""" This module contains the database model for the Account table."""

from datetime import datetime
from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey

from src.core.database import Base


class Account(Base):
    """
    Account model.
    """

    __tablename__ = "Account"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow, nullable=False)
    api_key = Column(String(255), nullable=False)
    role_id = Column(Integer, ForeignKey("Role.id"), nullable=True, default=0)
