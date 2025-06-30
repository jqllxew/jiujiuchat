from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker

from config import configs

engine = create_engine(configs.get_db_url)
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def _before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    print(f"--> SQL: {statement} | {parameters}")


event.listen(engine, "before_cursor_execute", _before_cursor_execute)


def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()
