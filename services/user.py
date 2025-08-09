from redis import Redis

from models.do.user import UserPrompt
from services import BaseService
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession


class UserService(BaseService):
    def __init__(self, db: AsyncSession,redis=Redis):
        super().__init__(db,redis)

    async def update_user_prompt(self, user_id: str, prompt: str) -> UserPrompt:
        """根据用户ID更新人设prompt"""
        # 检查是否存在记录
        stmt = select(UserPrompt).where(UserPrompt.user_id.__eq__(user_id))
        result = await self.db.execute(stmt)
        user_prompt = result.scalar_one_or_none()

        if user_prompt:
            # 更新现有记录
            user_prompt.prompt = prompt
            await self.db.commit()
            await self.db.refresh(user_prompt)
        else:
            # 创建新记录
            user_prompt = UserPrompt(
                user_id=user_id,
                prompt=prompt,
                title="用户人设"  # 可以根据需要修改
            )
            self.db.add(user_prompt)
            await self.db.commit()
            await self.db.refresh(user_prompt)

        return user_prompt

    async def create_user_prompt(self, user_id: str, prompt: str, title: str = "用户人设") -> UserPrompt:
        """创建新的用户人设"""
        user_prompt = UserPrompt(
            user_id=user_id,
            prompt=prompt,
            title=title,
            state="0"
        )
        self.db.add(user_prompt)
        await self.db.commit()
        # await self.db.refresh(user_prompt)
        return user_prompt

    async def get_user_prompt(self, user_id: str) -> UserPrompt | None:
        """根据用户id获取当前用户人设"""
        stmt = select(UserPrompt).where(UserPrompt.user_id.__eq__(user_id))
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def delete_user_prompt(self, user_id: str) -> bool:
        """删除用户人设"""
        stmt = delete(UserPrompt).where(UserPrompt.user_id.__eq__(user_id))
        result = await self.db.execute(stmt)
        await self.db.commit()
        return result.rowcount() > 0
