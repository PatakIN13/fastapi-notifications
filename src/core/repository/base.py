""" Base repository for all repositories """

from sqlalchemy import select, insert, update

from src.core.database import db_helper


class BaseRepository:
    """Base repository class."""

    model = None

    @classmethod
    async def find_by_id(cls, model_id: int):
        """Find model by id"""
        async with db_helper.session_factory() as session:
            query = select(cls.model).filter_by(id=model_id)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def find_one_or_none(cls, **kwargs):
        """Find one or none model by kwargs"""
        async with db_helper.session_factory() as session:
            query = select(cls.model).filter_by(**kwargs)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def get_all(cls) -> list:
        """Get all data from model."""
        async with db_helper.session_factory() as session:
            query = select(cls.model).order_by(cls.model.id)
            result = await session.execute(query)
            return list(result.scalars().all())

    @classmethod
    async def create(cls, **kwargs) -> int:
        """Create data in model."""
        async with db_helper.session_factory() as session:
            query = insert(cls.model).values(**kwargs)
            result = await session.execute(query)
            await session.commit()
            return result.lastrowid

    @classmethod
    async def update_data(cls, model_id: int, **kwargs) -> int:
        """Update data in model."""
        async with db_helper.session_factory() as session:
            query = update(cls.model).where(cls.model.id == model_id).values(**kwargs)
            await session.execute(query)
            await session.commit()
            return model_id
