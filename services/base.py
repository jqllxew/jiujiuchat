from typing import Any, Sequence

from redis.asyncio import Redis
from sqlalchemy import Select, select, func
from sqlalchemy.ext.asyncio import AsyncSession


class BaseService:
    def __init__(self, db: AsyncSession, redis: Redis):
        self.db = db
        self.redis = redis

    async def select_first(self, stmt: Select):
        result = await self.db.execute(stmt)
        return result.scalars().first()

    async def select_list(self, stmt: Select):
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def select_page(self, stmt: Select, page: int = 1, limit: int = 10) -> tuple[Sequence[Any], int]:
        total = await self.select_first(
            select(func.count()).select_from(stmt.subquery())
        )
        if total and isinstance(total, int):
            result_list = await self.select_list(stmt.limit(limit).offset((page-1) * limit))
            return result_list, total
        return [], 0
