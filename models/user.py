from sqlalchemy import Column, String, Integer

from models.base import Base, TimestampMixin


class User(Base, TimestampMixin):
    __tablename__ = "user"

    id = Column(String, primary_key=True, default=TimestampMixin.generate_id())
    union_id = Column(String, comment="微信唯一id")
    nickname = Column(String, comment="昵称")
    birth_year = Column(Integer, comment="出生年")
    gender = Column(Integer, comment="0男/1女")
