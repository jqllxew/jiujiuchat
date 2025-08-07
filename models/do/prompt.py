from models.do import SuperDO, Base
from sqlalchemy import Column, String, Integer, Text


class Prompt(Base, SuperDO):
    __tablename__ = "prompts"

    id: str= Column(String, primary_key=True, default=SuperDO.generate_id())
    prompt: str = Column(Text,comment="人设")
    title: str = Column(String,comment="标题")
    state: str = Column(String,comment="状态")