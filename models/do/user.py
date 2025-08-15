from pydantic import BaseModel
from sqlalchemy import Column, String, Integer, Text, DateTime,Boolean

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


class UserChatHistory(Base, SuperDO):
    __tablename__ = "user_chat_history"

    id = Column(String, primary_key=True, default=SuperDO.generate_id)
    user_id = Column(String,comment="用户id")
    content = Column(Text,comment="聊天记录")
    title = Column(String,comment="标题")
    state = Column(String,comment="状态")
    origin = Column(String,comment="来源")
    upload_time = Column(DateTime,comment="上传时间")

class UserChatImage(Base, SuperDO):
    __tablename__ = "user_chat_image"

    id = Column(String, primary_key=True, default=SuperDO.generate_id)
    user_id = Column(String,comment="用户id")
    chat_id = Column(String,comment="聊天id")
    image_id = Column(String,comment="图片id")


class UserPassionEvaluation(Base, SuperDO):
    __tablename__ = "user_passion_evaluation"

    id = Column(String, primary_key=True, default=SuperDO.generate_id)
    user_id = Column(String,comment="用户id")
    target_user_id = Column(String,comment="对象用户id,空为默认")
    trust: int = Column(Integer, comment="信任感")
    safety: int = Column(Integer, comment="安全感")
    communication: int = Column(Integer, comment="沟通")
    attunement: int = Column(Integer, comment="同频")
    repairability: int = Column(Integer, comment="修复力")
    intimacy: int = Column(Integer, comment="亲密度")

class UserPassionChangeRecord(Base, SuperDO):
    __tablename__ = "user_passion_change_record"

    id = Column(String, primary_key=True, default=SuperDO.generate_id)
    user_id = Column(String, comment="用户id")
    target_user_id = Column(String, comment="对象用户id,空为默认")
    passion_type: int = Column(Integer, comment="变更情感类型")
    value: int = Column(Integer, comment="变更值")
    change_time = Column(DateTime, comment="变更时间")

class UserMate(Base, SuperDO):
    __tablename__ = "user_mate"

    id = Column(String, primary_key=True, default=SuperDO.generate_id)
    user_id = Column(String, comment="用户id")
    mate_user_id = Column(String, comment="对象用户id,空为默认")
    is_show: bool = Column(Boolean, comment="是否展示朋友圈")

class UserEventRecord(Base, SuperDO):
    __tablename__ = "user_event_record"

    id = Column(String, primary_key=True, default=SuperDO.generate_id)
    user_id = Column(String,comment="用户id")
    content = Column(Text,comment="记录内容")
    title = Column(String,comment="标题")
    show_type = Column(String,default ="0",comment="显示类型 0:公开，1:自己")


