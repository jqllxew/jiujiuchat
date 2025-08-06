from datetime import datetime

from sqlalchemy import Column, DateTime
from sqlalchemy.orm import declarative_base
from snowflake import SnowflakeGenerator

Base = declarative_base()
generator = SnowflakeGenerator(1)


class TimestampMixin:
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    @staticmethod
    def generate_id():
        return str(next(generator))
