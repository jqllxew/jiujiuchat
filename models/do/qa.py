import enum
from typing import Optional

from sqlalchemy import Column, String, Text, ARRAY, Float, Integer, BigInteger, Numeric
from sqlalchemy.dialects.postgresql import JSONB

from models.do import SuperDO, Base
from models.enum import Dimensional


class QuestionnaireGroup(Base, SuperDO):
    __tablename__ = "questionnaire_group"

    id: Optional[str] = Column(String, primary_key=True, default=SuperDO.generate_id)
    name: Optional[str] = Column(String, unique=True, nullable=False, comment="组名")
    weights: Optional[dict] = Column(JSONB, nullable=True, default=None, comment="维度权重")
    sub_name: Optional[str] = Column(String, nullable=True, comment="子组名")
    sub_name_en: Optional[str] = Column(String, nullable=True, comment="子组名英文")
    sort: Optional[int] = Column(Integer, nullable=True, default=0, comment="排序")


class Questionnaire(Base, SuperDO):
    __tablename__ = "questionnaire"

    id: Optional[str] = Column(String, primary_key=True, default=SuperDO.generate_id)
    group_id: Optional[str] = Column(String, nullable=True, comment="问题组ID")
    question: Optional[str] = Column(String, nullable=False, comment="问题描述")
    question_content: Optional[str] = Column(Text, nullable=False, comment="问题内容")
    answer: Optional[list] = Column(ARRAY(String), nullable=False, comment="答案选项")
    answer_extreme: Optional[list] = Column(ARRAY(String), comment="答案两端倾向")
    sort: Optional[int] = Column(Integer, nullable=True, default=0, comment="排序")


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
    score: float = Column(Numeric(4, 1), nullable=False, comment="分数")
