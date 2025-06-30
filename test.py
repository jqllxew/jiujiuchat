from sqlalchemy import text
from db import get_db

if __name__ == "__main__":
    db_gen = get_db()
    db = next(db_gen)
    res = db.execute(text("SELECT version();"))
    for row in res:
        print("PostgreSQL 版本:", row[0])
