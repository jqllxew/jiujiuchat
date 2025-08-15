from pydantic import BaseModel
from sqlalchemy import Column, String, Integer, Text,Float

from .base import Base, SuperDO


class UserRank(Base, SuperDO):
    __tablename__ = "user_rank"

    id: str = Column(String, primary_key=True, default=SuperDO.generate_id)
    name: str = Column(String, unique=True, comment="用户等级")
    description: str = Column(String, comment="等级描述")
    level: int = Column(Integer, comment="等级级别")
    required_price: int = Column(Integer, comment="价格，分为单位")
    preferential_price: int = Column(Integer, comment="优惠价格，分为单位")
    renewal_price: int = Column(Integer, comment="续费价格，分为单位")
    duration: int = Column(Integer, comment="有效期，天为单位，0表示永不过期")


class UserRankPrompt(Base, SuperDO):
    __tablename__ = "user_rank_prompt"

    id: str = Column(String, primary_key=True, default=SuperDO.generate_id)
    user_rank_id: str = Column(String, comment="用户等级id")
    prompt_id: str = Column(String, comment="提示词")

class UserRankFunc(Base, SuperDO):
    __tablename__ = "user_rank_func"

    id: str = Column(String, primary_key=True, default=SuperDO.generate_id)
    user_rank_id: str = Column(String, comment="用户等级id")
    function_id: str = Column(String, comment="功能id")



