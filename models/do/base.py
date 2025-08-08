import threading
from datetime import datetime
from typing import Type, TypeVar

from pydantic import BaseModel
from sqlalchemy import Column, DateTime
from sqlalchemy.orm import declarative_base, DeclarativeBase
from config.id import Snowflake

snowflake = Snowflake(1, 1)
Base = declarative_base()
T = TypeVar("T", bound="SuperDO")


class SuperDO:
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)

    @staticmethod
    def generate_id():
        return str(snowflake.next_id())

    @classmethod
    def from_vo(cls: Type[T], vo: BaseModel) -> T:
        vo_dict = vo.model_dump()
        do_fields = {c.key for c in cls.__table__.columns}
        filtered_data = {k: v for k, v in vo_dict.items() if k in do_fields}
        return cls(**filtered_data)
