from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from redis.asyncio import Redis

from models.do.prompt import Prompts
from services.base import BaseService


class PromptService(BaseService):
    def __init__(self, db: AsyncSession, redis: Redis):
        super().__init__(db, redis)

    async def create_prompt(self, prompt: str, title: str) -> Prompts:
        """创建新的人设prompt"""
        prompt_obj = Prompts(
            prompt=prompt,
            title=title,
            state="0"
        )
        self.db.add(prompt_obj)
        await self.db.commit()
        await self.db.refresh(prompt_obj)
        return prompt_obj

    async def get_prompt(self, prompt_id: str) -> Prompts | None:
        """根据ID获取prompt"""
        stmt = select(Prompts).where(Prompts.id == prompt_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_all_prompts(self, state: str = None) -> list[Prompts]:
        """获取所有prompt，可按状态筛选"""
        stmt = select(Prompts)
        if state:
            stmt = stmt.where(Prompts.state == state)
        stmt = stmt.order_by(Prompts.created_at.desc())
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def update_prompt(self, prompt_id: str, **kwargs) -> Prompts | None:
        """更新prompt"""
        stmt = (
            update(Prompts)
            .where(Prompts.id == prompt_id)
            .values(**{k: v for k, v in kwargs.items() if v is not None})
            .execution_options(synchronize_session="fetch")
        )
        await self.db.execute(stmt)
        await self.db.commit()
        return await self.get_prompt(prompt_id)

    async def delete_prompt(self, prompt_id: str) -> bool:
        """删除prompt（软删除，修改状态）"""
        prompt = await self.get_prompt(prompt_id)
        if prompt:
            prompt.state = "deleted"
            await self.db.commit()
            return True
        return False

    async def hard_delete_prompt(self, prompt_id: str) -> bool:
        """硬删除prompt"""
        stmt = delete(Prompts).where(Prompts.id == prompt_id)
        result = await self.db.execute(stmt)
        await self.db.commit()
        return result.rowcount > 0
