import enum

from sqlalchemy import Column, String, Text
from .base import SuperDO, Base


class SessionRole(enum.Enum):
    ASST = "asst"
    USER = "user"
    SYSTEM = "system"


class Client(Base, SuperDO):
    __tablename__ = "ai_client"

    id = Column(String, primary_key=True, default=SuperDO.generate_id())
    api_key = Column(String, unique=True, nullable=False, comment="API Key")
    base_url = Column(String, nullable=False, comment="api域名")
    proxy = Column(String, nullable=True, comment="代理")


class Session(Base, SuperDO):
    __tablename__ = "ai_session"

    id = Column(String, primary_key=True, default=SuperDO.generate_id())
    role = Column(String, comment="类型 user/asst")
    content = Column(Text, comment="内容")
