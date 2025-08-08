from sqlalchemy import Column, String, Text, ARRAY

from models.do import SuperDO, Base


class Evaluate(Base,SuperDO):
    __tablename__ = "evaluate"

    id: str = Column(String, primary_key=True, default=SuperDO.generate_id)
    question_groups : str = Column(Text, nullable=False)
    question: str = Column(Text, nullable=False)
    answer: str = Column(ARRAY(String), nullable=False)
