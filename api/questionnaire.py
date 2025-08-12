
from fastapi import APIRouter, Depends, Query, HTTPException, Path

from models.vo.base import Result, Page
from models.vo.questionnaire import (
    QuestionnaireResponse,
    QuestionnaireSearchRequest,
    QuestionnaireSaveReq,
    QuestionnaireAnswersReq
)
from services import QuestionnaireService, get_service, get_system_user, get_app_user

router = APIRouter()


@router.post("", response_model=Result[QuestionnaireResponse], summary="保存问卷项(管理端)")
async def save_questionnaire(
    req: QuestionnaireSaveReq,
    questionnaire_service: QuestionnaireService = Depends(get_service(QuestionnaireService)),
    _=Depends(get_system_user)
):
    m = await questionnaire_service.save_questionnaire(req)
    return Result.success_(QuestionnaireResponse.from_do(m))


@router.get("", response_model=Result[Page], summary="获取问卷列表(app)")
async def get_questionnaires(
    *,
    req: QuestionnaireSearchRequest = Depends(),
    questionnaire_service: QuestionnaireService = Depends(get_service(QuestionnaireService))
):
    """获取评估记录列表，支持分页"""
    result, total = await questionnaire_service.get_questionnaires(req)
    return Result.success_(
        Page[QuestionnaireResponse](
            total=total,
            items=[QuestionnaireResponse.from_do(e) for e in result]
        )
    )


@router.post("/answer", response_model=Result[QuestionnaireResponse], summary="提交问卷答案(app)")
async def answer_questionnaire(
    *,
    req: QuestionnaireAnswersReq,
    questionnaire_service: QuestionnaireService = Depends(get_service(QuestionnaireService)),
    userinfo: dict = Depends(get_app_user)
):
    if not req.user_id:
        req.user_id = userinfo.get("id")
    await questionnaire_service.save_user_answers(req)
    return Result.success_(msg="提交成功")

# @router.put("/{evaluate_id}", response_model=Result[QuestionnaireResponse], summary="更新评估记录")
# async def update_evaluate(
#         evaluate_id: str,
#         request: QuestionnaireUpdateRequest,
#         evaluate_service: QuestionnaireService = Depends(get_service(QuestionnaireService))
# ):
#     """更新评估记录"""
#     evaluate = await evaluate_service.update_evaluate(
#         evaluate_id=evaluate_id,
#         **request.model_dump(exclude_unset=True)
#     )
#     if not evaluate:
#         return Result.error_("评估记录不存在")
#     return Result.success_(QuestionnaireResponse.from_do(evaluate))


@router.delete("/{evaluate_id}", summary="删除问卷项(管理端)")
async def delete_evaluate(
    evaluate_id: str,
    evaluate_service: QuestionnaireService = Depends(get_service(QuestionnaireService)),
    _=Depends(get_system_user)
):
    """删除评估记录"""
    success = await evaluate_service.delete_questionnaire(evaluate_id)
    if not success:
        return Result.error_("评估记录不存在")
    return Result.success_(msg="删除成功")
