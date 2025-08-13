from pydantic import BaseModel
from sqlalchemy import Column, String, Integer, Text

from .base import Base, SuperDO


class User(Base, SuperDO):
    __tablename__ = "users"

    id: str = Column(String, primary_key=True, default=SuperDO.generate_id)
    phone: str = Column(String, unique=True, comment="手机号")
    passwd: str = Column(String, comment="密码")
    union_id: str = Column(String, comment="微信唯一id")
    nickname: str = Column(String, comment="昵称")
    birth_year: int = Column(Integer, comment="出生年")
    gender: int = Column(Integer, comment="0男/1女")
    type: str = Column(String,comment="用户类型")


class UserPrompt(Base, SuperDO):
    __tablename__ = "user_prompt"

    id = Column(String, primary_key=True, default=SuperDO.generate_id)
    user_id = Column(String,comment="用户id")
    prompt = Column(Text,comment="人设")
    title = Column(String,comment="标题")
    state = Column(String,comment="状态")

