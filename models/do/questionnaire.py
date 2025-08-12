import enum
from typing import Optional

from sqlalchemy import Column, String, Text, ARRAY, Float
from sqlalchemy.dialects.postgresql import JSONB

from models.do import SuperDO, Base


class Dimensional(enum.Enum):
    """维度枚举"""
    COMMUNICATION = "Communication"  # 沟通
    SAFETY = "Safety"  # 安全感
    INTIMACY = "Intimacy"  # 亲密度
    ATTUNEMENT = "Attunement"  # 同频
    TRUST = "Trust"  # 信任
    REPAIRABILITY = "Repairability"  # 修复能力


class Questionnaire(Base, SuperDO):
    __tablename__ = "questionnaire"

    id: Optional[str] = Column(String, primary_key=True, default=SuperDO.generate_id)
    question_groups: Optional[str] = Column(String, nullable=False, comment="问题组")
    question: Optional[str] = Column(String, nullable=False, comment="问题描述")
    question_content: Optional[str] = Column(Text, nullable=False, comment="问题内容")
    answer: Optional[list] = Column(ARRAY(String), nullable=False, comment="答案选项")
    answer_extreme: Optional[list] = Column(ARRAY(String), comment="答案两端倾向")
    weights: Optional[list] = Column(JSONB, comment="维度权重")


class UserQuestionnaire(Base, SuperDO):
    __tablename__ = "user_questionnaire"

    id: Optional[str] = Column(String, primary_key=True, default=SuperDO.generate_id)
    user_id: Optional[str] = Column(String, nullable=False, comment="用户ID")
    questionnaire_id: Optional[str] = Column(String, nullable=False, comment="问卷项ID")
    answer: Optional[list] = Column(ARRAY(String), comment="用户答案")


class UserDimensional(Base, SuperDO):
    __tablename__ = "user_dimensional"

    id: str = Column(String, primary_key=True, default=SuperDO.generate_id)
    user_id: str = Column(String, nullable=False, comment="用户ID")
    dimensional: Dimensional = Column(String, nullable=False, comment="维度")
    score: float = Column(Float, nullable=False, comment="分数")
