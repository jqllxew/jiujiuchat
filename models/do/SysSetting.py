from pydantic import BaseModel
from sqlalchemy import Column, String, Integer, Text,Float,Boolean
from .base import Base, SuperDO


class SysConfig(Base, SuperDO):
    __tablename__ = "sys_config"

    id: str = Column(String, primary_key=True, default=SuperDO.generate_id)
    description: str = Column(String, comment="配置描述")
    key: str = Column(String, comment="配置key")
    value: str = Column(String, comment="配置value")
    group: str = Column(String, comment="配置分组")


class AiKey(Base, SuperDO):
    __tablename__ = "ai_key"

    id: str = Column(String, primary_key=True, default=SuperDO.generate_id)
    description: str = Column(String, comment="描述")
    key: str = Column(String, comment="key")
    ai_type: str = Column(String, comment="gpt、claude、deepseek")
    balance: int = Column(Integer, comment="余额，分为单位")
    seq: int = Column(Integer, comment="序号，多个key时候可以按照序号排序使用")
    is_enable: bool = Column(Boolean, default=True, comment="是否启用")





