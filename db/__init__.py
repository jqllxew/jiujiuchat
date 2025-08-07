import logging

from sqlalchemy import event
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from config import configs
from redis.asyncio import Redis
from fastapi import Request

_engine = create_async_engine(configs.get_db_url)
_session = sessionmaker(  # type: ignore
    bind=_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


redis_client = Redis(
    host=configs.REDIS_SERVER,
    port=configs.REDIS_PORT,
    password=configs.REDIS_PASSWORD,
    db=configs.REDIS_DATABASE,
    decode_responses=True,
)


def _before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    logging.info(f"SQL: {statement} | {parameters}")


event.listen(_engine.sync_engine, "before_cursor_execute", _before_cursor_execute)


async def get_db():
    async with _session() as db:
        yield db


async def get_redis(req: Request) -> Redis:
    return req.app.state.redis


async def dispose():
    await _engine.dispose()
    await redis_client.close()
