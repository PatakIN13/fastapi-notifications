""" This module contains the Role model."""

from sqlalchemy import Column, Integer, String

from src.core.database import Base


class Role(Base):
    """
    Role model.
    """

    __tablename__ = "Role"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(10), nullable=False)
