import asyncio

from sqlalchemy import text
from db import get_db


async def test():
    gen = get_db()
    db = await gen.__anext__()
    res = await db.execute(text("SELECT version();"))
    for row in res:
        print("version: ", row[0])


if __name__ == "__main__":
    asyncio.run(test())

