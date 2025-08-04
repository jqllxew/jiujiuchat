from sqlalchemy import Column, String, Integer, Text

from models.base import Base, TimestampMixin


class User(Base, TimestampMixin):
    __tablename__ = "user"

    id = Column(String, primary_key=True, default=TimestampMixin.generate_id())
    union_id = Column(String, comment="微信唯一id")
    nickname = Column(String, comment="昵称")
    birth_year = Column(Integer, comment="出生年")
    gender = Column(Integer, comment="0男/1女")

class UserPrompt(Base,TimestampMixin):
    __tablename__ = "user_prompt"


    id = Column(String, primary_key=True, default=TimestampMixin.generate_id())
    user_id = Column(String,comment="用户id")
    prompt = Column(Text,comment="人设")
    title = Column(String,comment="标题")

