from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker

from config import configs

_engine = create_engine(configs.get_db_url)
_session = sessionmaker(
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
    bind=_engine,
)


def _before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    print(f"--> SQL: {statement} | {parameters}")


event.listen(_engine, "before_cursor_execute", _before_cursor_execute)


def get_db():
    db = _session()
    try:
        yield db
    finally:
        db.close()


def dispose():
    _engine.dispose()
