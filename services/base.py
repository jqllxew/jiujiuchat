from sqlalchemy import Select
from sqlalchemy.ext.asyncio import AsyncSession


class BaseService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def select_first(self, stmt: Select):
        result = await self.db.execute(stmt)
        return result.scalars().first()

    async def select_list(self, stmt: Select):
        result = await self.db.execute(stmt)
        return result.scalars().all()
