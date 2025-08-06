import openai
from openai import AsyncOpenAI
from sqlalchemy.ext.asyncio import AsyncSession

from services.base import BaseService


class ChatService(BaseService):

    def __init__(self, db: AsyncSession):
        super().__init__(db)
        self.client = AsyncOpenAI()

    async def chat(self):
        ...

    async def steam(self, model, current_msg, temperature: float):
        response = await openai.ChatCompletion.acreate(
            model=model,
            messages=[
            ],
            temperature=temperature,
            stream=True
        )
        async for chunk in response:
            if "choices" in chunk:
                delta = chunk["choices"][0].get("delta", {})
                content = delta.get("content")
                if content:
                    yield content
        ...
