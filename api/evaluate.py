from fastapi import APIRouter, Depends, Query, HTTPException

from models.vo.evaluate import (
    EvaluateCreateRequest,
    EvaluateUpdateRequest,
    EvaluateResponse,
    EvaluateListResponse,
    EvaluateSearchRequest
)
from services import EvaluateService, get_service

router = APIRouter()

@router.post("", response_model=EvaluateResponse, summary="创建评估记录")
async def create_evaluate(
        request: EvaluateCreateRequest,
        evaluate_service: EvaluateService = Depends(get_service(EvaluateService))
) -> EvaluateResponse:
    """创建新的评估记录"""
    evaluate = await evaluate_service.create_evaluate(
        question_groups=request.question_groups,
        question_content=request.question_content,
        question=request.question,
        answer=request.answer
    )
    return EvaluateResponse.from_do(evaluate)


@router.get("/{evaluate_id}", response_model=EvaluateResponse, summary="获取评估记录")
async def get_evaluate(
        evaluate_id: str,
        evaluate_service: EvaluateService = Depends(get_service(EvaluateService))
) -> EvaluateResponse:
    """根据ID获取评估记录"""
    evaluate = await evaluate_service.get_evaluate(evaluate_id)
    if not evaluate:
        raise HTTPException(status_code=404, detail="评估记录不存在")
    return EvaluateResponse.from_do(evaluate)


@router.get("", response_model=EvaluateListResponse, summary="获取评估记录列表")
async def get_evaluates(
        limit: int = Query(100, ge=1, le=1000, description="每页数量"),
        offset: int = Query(0, ge=0, description="偏移量"),
        evaluate_service: EvaluateService = Depends(get_service(EvaluateService))
) -> EvaluateListResponse:
    """获取评估记录列表，支持分页"""
    evaluates = await evaluate_service.get_all_evaluates(limit=limit, offset=offset)
    return EvaluateListResponse(
        total=len(evaluates),
        items=[EvaluateResponse.from_do(e) for e in evaluates]
    )


@router.put("/{evaluate_id}", response_model=EvaluateResponse, summary="更新评估记录")
async def update_evaluate(
        evaluate_id: str,
        request: EvaluateUpdateRequest,
        evaluate_service: EvaluateService = Depends(get_service(EvaluateService))
) -> EvaluateResponse:
    """更新评估记录"""
    evaluate = await evaluate_service.update_evaluate(
        evaluate_id=evaluate_id,
        **request.dict(exclude_unset=True)
    )
    if not evaluate:
        raise HTTPException(status_code=404, detail="评估记录不存在")
    return EvaluateResponse.from_do(evaluate)


@router.delete("/{evaluate_id}", summary="删除评估记录")
async def delete_evaluate(
        evaluate_id: str,
        evaluate_service: EvaluateService = Depends(get_service(EvaluateService))
) -> dict:
    """删除评估记录"""
    success = await evaluate_service.delete_evaluate(evaluate_id)
    if not success:
        raise HTTPException(status_code=404, detail="评估记录不存在")
    return {"success": True, "message": "删除成功"}


@router.post("/search", response_model=EvaluateListResponse, summary="搜索评估记录")
async def search_evaluates(
        request: EvaluateSearchRequest,
        limit: int = Query(100, ge=1, le=1000, description="每页数量"),
        offset: int = Query(0, ge=0, description="偏移量"),
        evaluate_service: EvaluateService = Depends(get_service(EvaluateService))
) -> EvaluateListResponse:
    """搜索评估记录"""
    if request.question_keyword:
        evaluates = await evaluate_service.search_by_question(request.question_keyword)
    elif request.groups_keyword:
        evaluates = await evaluate_service.search_by_groups(request.groups_keyword)
    else:
        evaluates = await evaluate_service.get_all_evaluates(limit=limit, offset=offset)

    return EvaluateListResponse(
        total=len(evaluates),
        items=[EvaluateResponse.from_do(e) for e in evaluates[offset:offset + limit]]
    )