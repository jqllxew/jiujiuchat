from pydantic import BaseModel
from sqlalchemy import Column, String, Integer, Text,Float

from .base import Base, SuperDO


class func(Base, SuperDO):
    __tablename__ = "func"

    id: str = Column(String, primary_key=True, default=SuperDO.generate_id)
    name: str = Column(String, unique=True, comment="功能名称")
    description: str = Column(String, comment="功能描述")
    func_key: str = Column(String, unique=True, comment="功能key")
    usage_times: int = Column(Integer, comment="单次购买授权次数")
    once_price: int = Column(Integer, comment="单次价格，分为单位")
    preferential_once_price: int = Column(Integer, comment="优惠单词价格，分为单位")
    status: int = Column(Integer, comment="是否有效，0无效，1有效")





