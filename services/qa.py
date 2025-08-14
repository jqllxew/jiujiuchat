from sqlalchemy import select, update, delete, func, inspect
from typing import List, Sequence

from sqlalchemy import select, update, delete

from config.exc import ServiceException
from models.do.qa import Questionnaire, UserQuestionnaire, QuestionnaireGroup
from models.vo.qa import QuestionnaireSearchRequest, QuestionnaireSaveReq, QuestionnaireAnswersReq, \
    GroupResp, QuestionnaireResponse
from services.base import BaseService


class QuestionnaireService(BaseService):

    async def _save_group(self, group_name: str, weights: List[str] = None, sub_name: str = None,
                          sub_name_en: str = None, group_sort: int = None) -> QuestionnaireGroup:
        """保存或更新问卷组"""
        group = await self.select_first(select(QuestionnaireGroup).where(
            QuestionnaireGroup.name.__eq__(group_name)
        ))
        if group:
            stmt = (
                update(QuestionnaireGroup)
                .where(QuestionnaireGroup.id.__eq__(group.id))
                .values(name=group_name,
                        weights=weights if weights is not None else group.weights
            ))
            await self.db.execute(stmt)
        else:
            group = QuestionnaireGroup(
                name=group_name, weights=weights,
                sub_name=sub_name, sub_name_en=sub_name_en,
                sort=group_sort)
            self.db.add(group)
        await self.db.commit()
        return group

    async def save_questionnaire(self, req: QuestionnaireSaveReq) -> Questionnaire:
        """保存问卷项"""
        group = await self._save_group(req.group_name, req.weights, req.sub_name, req.sub_name_en, req.group_sort)
        evaluate = Questionnaire.from_vo(req)
        evaluate.group_id = group.id
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
                .values(**evaluate.to_update_dict())
            )
            await self.db.execute(stmt)
        else:
            evaluate.id = None
            self.db.add(evaluate)
        await self.db.commit()
        return evaluate

    async def get_questionnaires(self, req: QuestionnaireSearchRequest) -> tuple[list, int]:
        """获取所有评估记录，支持分页"""
        groups, total = await self.select_page(select(QuestionnaireGroup).order_by(
            QuestionnaireGroup.sort.asc(),
            QuestionnaireGroup.id.asc()
        ), req.page, req.limit)
        if not groups:
            return [], 0
        # 获取 每个组下的问卷项
        group_dict = {g.id: g for g in groups}
        group_ids = list(group_dict.keys())
        stmt = select(Questionnaire).where(
            Questionnaire.group_id.in_(group_ids)
        ).order_by(
            Questionnaire.sort.asc(),
            Questionnaire.id.asc()
        )
        questionnaires = await self.select_list(stmt)
        # 将问卷项按组分类
        result = []
        for group in groups:
            group_qs = [q for q in questionnaires if q.group_id == group.id]
            group_resp = GroupResp.from_do(group)
            group_resp.qs = [QuestionnaireResponse.from_do(q) for q in group_qs]
            result.append(group_resp)
        return result, total

    async def save_user_answers(self, req: QuestionnaireAnswersReq):
        qa = await self.select_list(select(Questionnaire))
        qa_dict = {q.id: q for q in qa}
        qas = []
        for a in req.answers:
            _qa = qa_dict.get(a.id)
            if not _qa:
                raise ServiceException(f"问卷项 {a.id} 不存在")
            if not set(a.answer).issubset(_qa.answer):
                raise ServiceException(f"答案 {a.answer} 不在问卷项 {_qa.id} 的答案列表中")
            user_qa = await self.select_first(select(UserQuestionnaire).where(
                UserQuestionnaire.user_id.__eq__(req.user_id) &
                UserQuestionnaire.questionnaire_id.__eq__(_qa.id)
            ))
            if user_qa:
                # 更新用户答案
                stmt = (
                    update(UserQuestionnaire)
                    .where(UserQuestionnaire.id.__eq__(user_qa.id))
                    .values(answer=a.answer)
                )
                await self.db.execute(stmt)
            else:
                # 新增用户答案
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
