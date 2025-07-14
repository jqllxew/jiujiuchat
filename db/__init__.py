from sqlalchemy import event
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from config import configs

_engine = create_async_engine(configs.get_db_url)
_session = sessionmaker(  # type: ignore
    bind=_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


def _before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    print(f"--> SQL: {statement} | {parameters}")


event.listen(_engine.sync_engine, "before_cursor_execute", _before_cursor_execute)


async def get_db():
    async with _session() as db:
        yield db


def dispose():
    _engine.dispose()
