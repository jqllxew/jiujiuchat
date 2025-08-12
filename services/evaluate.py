from sqlalchemy import select, update, delete, func, inspect
from typing import List, Sequence

from sqlalchemy import select, update, delete

from config.exc import ServiceException
from models.do.questionnaire import Questionnaire, UserQuestionnaire
from models.vo.questionnaire import QuestionnaireSearchRequest, QuestionnaireSaveReq, QuestionnaireAnswersReq
from services.base import BaseService


class QuestionnaireService(BaseService):

    async def save_questionnaire(self, req: QuestionnaireSaveReq) -> Questionnaire:
        """保存问卷项"""
        evaluate = Questionnaire.from_vo(req)
        if evaluate.id:
            # 更新操作
            cnt = await self.select_first(select(func.count()).select_from(Questionnaire).where(
                Questionnaire.id.__eq__(evaluate.id)
            ))
            if cnt == 0:
                raise ServiceException("问卷项不存在")
            # 更新现有记录
            stmt = (
                update(Questionnaire)
                .where(Questionnaire.id.__eq__(evaluate.id))
                .values(**evaluate.to_dict())
            )
            await self.db.execute(stmt)
        else:
            evaluate.id = None
            self.db.add(evaluate)
        await self.db.commit()
        return evaluate

    # async def get_questionnaire(self, evaluate_id: str) -> Questionnaire | None:
    #     """根据ID获取评估记录"""
    #     stmt = select(Questionnaire).where(Questionnaire.id.__eq__(evaluate_id))
    #     result = await self.db.execute(stmt)
    #     return result.scalar_one_or_none()

    async def get_questionnaires(self, req: QuestionnaireSearchRequest) -> tuple[Sequence[Questionnaire], int]:
        """获取所有评估记录，支持分页"""
        conditions = []
        if req.question_groups:
            conditions.append(Questionnaire.question_groups.contains(req.question_groups))
        if req.question:
            conditions.append(Questionnaire.question.contains(req.question))
        if req.question_content:
            conditions.append(Questionnaire.question_content.contains(req.question_content))
        result, total = await self.select_page(select(Questionnaire).where(
            *conditions
        ).order_by(Questionnaire.id.asc()), req.page, req.limit)
        return result, total

    async def save_user_answers(self, req: QuestionnaireAnswersReq):
        qa = await self.select_list(select(Questionnaire))
        qa_dict = {q.id: q for q in qa}
        qas = []
        for a in req.answers:
            _qa = qa_dict.get(a.id)
            if not _qa:
                raise ServiceException(f"问卷项 {a.id} 不存在")
            if a.answer not in _qa.answer:
                raise ServiceException(f"答案 {a.answer} 不在问卷项 {_qa.id} 的答案列表中")
            user_qa = UserQuestionnaire(
                user_id=req.user_id,
                questionnaire_id=_qa.id,
                answer=a.answer
            )
            qas.append(user_qa)
        if qas:
            self.db.add_all(qas)
            await self.db.commit()

        # 计算并保存维度分数



    async def delete_questionnaire(self, evaluate_id: str) -> bool:
        """删除评估记录"""
        stmt = delete(Questionnaire).where(Questionnaire.id.__eq__(evaluate_id))
        result = await self.db.execute(stmt)
        await self.db.commit()
        return result.rowcount() > 0
