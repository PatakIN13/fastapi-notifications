""" Role schemas. """

from pydantic import BaseModel, ConfigDict


class RoleBase(BaseModel):
    """Account base schema."""

    name: str


class RoleCreate(RoleBase):
    """Account create schema."""

    pass


class Role(RoleBase):
    """Account schema."""

    model_config = ConfigDict(from_attributes=True)
    id: int
