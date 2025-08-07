import threading
from datetime import datetime
from typing import Type, TypeVar

from pydantic import BaseModel
from sqlalchemy import Column, DateTime
from sqlalchemy.orm import declarative_base
from snowflake import SnowflakeGenerator

Base = declarative_base()
generator = SnowflakeGenerator(1)
T = TypeVar("T", bound="SuperDO")

_lock = threading.Lock()


class SuperDO:
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    @staticmethod
    def generate_id():
        with _lock:
            return str(next(generator))

    @classmethod
    def from_vo(cls: Type[T], vo: BaseModel) -> T:
        vo_dict = vo.model_dump()
        do_fields = {c.key for c in cls.__table__.columns}
        filtered_data = {k: v for k, v in vo_dict.items() if k in do_fields}
        return cls(**filtered_data)
