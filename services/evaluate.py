from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from redis.asyncio import Redis
from typing import List, Optional

from models.do.evaluate import Evaluate
from services.base import BaseService


class EvaluateService(BaseService):
    def __init__(self, db: AsyncSession, redis: Redis):
        super().__init__(db, redis)

    async def create_evaluate(self, question_groups: str, question: str, answer: List[str]) -> Evaluate:
        """创建新的评估记录"""
        evaluate = Evaluate(
            question_groups=question_groups,
            question=question,
            answer=answer
        )
        self.db.add(evaluate)
        await self.db.commit()
        await self.db.refresh(evaluate)
        return evaluate

    async def get_evaluate(self, evaluate_id: str) -> Evaluate | None:
        """根据ID获取评估记录"""
        stmt = select(Evaluate).where(Evaluate.id == evaluate_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_all_evaluates(self, limit: int = 100, offset: int = 0) -> List[Evaluate]:
        """获取所有评估记录，支持分页"""
        stmt = select(Evaluate).order_by(Evaluate.created_at.desc()).limit(limit).offset(offset)
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def update_evaluate(self, evaluate_id: str, **kwargs) -> Evaluate | None:
        """更新评估记录"""
        stmt = (
            update(Evaluate)
            .where(Evaluate.id == evaluate_id)
            .values(**{k: v for k, v in kwargs.items() if v is not None})
            .execution_options(synchronize_session="fetch")
        )
        await self.db.execute(stmt)
        await self.db.commit()
        return await self.get_evaluate(evaluate_id)

    async def delete_evaluate(self, evaluate_id: str) -> bool:
        """删除评估记录"""
        stmt = delete(Evaluate).where(Evaluate.id == evaluate_id)
        result = await self.db.execute(stmt)
        await self.db.commit()
        return result.rowcount > 0

    async def search_by_question(self, question_keyword: str) -> List[Evaluate]:
        """根据问题关键词搜索"""
        stmt = select(Evaluate).where(
            Evaluate.question.contains(question_keyword)
        ).order_by(Evaluate.created_at.desc())
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def search_by_groups(self, groups_keyword: str) -> List[Evaluate]:
        """根据问题组关键词搜索"""
        stmt = select(Evaluate).where(
            Evaluate.question_groups.contains(groups_keyword)
        ).order_by(Evaluate.created_at.desc())
        result = await self.db.execute(stmt)
        return result.scalars().all()