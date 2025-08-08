import enum

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


class Evaluate(Base, SuperDO):
    __tablename__ = "evaluate"

    id: str = Column(String, primary_key=True, default=SuperDO.generate_id)
    question_groups: str = Column(Text, nullable=False)
    question: str = Column(Text, nullable=False)
    question_content: str = Column(Text, nullable=False)
    answer: list = Column(ARRAY(String), nullable=False)
    # 关联维度权重字段 {维度: 权重}
    weights: list[dict] = Column(JSONB, comment="维度权重")


class UserEvaluate(Base, SuperDO):
    __tablename__ = "user_evaluate"

    id: str = Column(String, primary_key=True, default=SuperDO.generate_id)
    user_id: str = Column(String, nullable=False, comment="用户ID")
    evaluate_id: str = Column(String, nullable=False, comment="评估ID")
    answer: str = Column(String, comment="用户答案")


class UserDimensional(Base, SuperDO):
    __tablename__ = "user_dimensional"

    id: str = Column(String, primary_key=True, default=SuperDO.generate_id)
    user_id: str = Column(String, nullable=False, comment="用户ID")
    dimensional: Dimensional = Column(String, nullable=False, comment="维度")
    score: float = Column(Float, nullable=False, comment="分数")
    # evaluate_ids: list[str] = Column(ARRAY(String), nullable=False, comment="关联评估ID列表")
