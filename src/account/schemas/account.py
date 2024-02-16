""" Account schemas. """

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class AccountBase(BaseModel):
    """Account base schema."""

    name: str


class AccountRole(BaseModel):
    """Account role schema."""

    role_id: int


class AccountCreate(AccountBase, AccountRole):
    """Account create schema."""

    pass


class Account(AccountBase, AccountRole):
    """Account schema."""

    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: datetime
    api_key: str
