""" Account schemas. """

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class AccountBase(BaseModel):
    """Account base schema."""

    name: str


class AccountCreate(AccountBase):
    """Account create schema."""

    pass


class Account(AccountBase):
    """Account schema."""

    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: datetime
    api_key: str
