from http.client import HTTPException

from fastapi import APIRouter, Depends, Query
from typing import Optional, List

from models.vo.prompt import (
    PromptCreateRequest,
    PromptUpdateRequest,
    PromptResponse,
    PromptListResponse
)
from services import PromptService, get_service

router = APIRouter()


@router.post("", response_model=PromptResponse, summary="创建人设")
async def create_prompt(
    request: PromptCreateRequest,
    prompt_service: PromptService = Depends(get_service(PromptService))
) -> PromptResponse:
    """创建新的人设prompt"""
    prompt = await prompt_service.create_prompt(
        prompt=request.prompt,
        title=request.title,
        # state=request.state
    )
    return PromptResponse.from_do(prompt)


@router.get("/{prompt_id}", response_model=PromptResponse, summary="获取人设详情")
async def get_prompt(
    prompt_id: str,
    prompt_service: PromptService = Depends(get_service(PromptService))
) -> PromptResponse:
    """根据ID获取人设详情"""
    prompt = await prompt_service.get_prompt(prompt_id)
    if not prompt:
        raise HTTPException(status_code=404, detail="人设不存在")
    return PromptResponse.from_do(prompt)


@router.get("", response_model=PromptListResponse, summary="获取人设列表")
async def get_prompts(
    state: Optional[str] = Query(None, description="按状态筛选"),
    prompt_service: PromptService = Depends(get_service(PromptService))
) -> PromptListResponse:
    """获取所有人设列表"""
    prompts = await prompt_service.get_all_prompts(state=state)
    return PromptListResponse(
        total=len(prompts),
        items=[PromptResponse.from_do(p) for p in prompts]
    )


@router.put("/{prompt_id}", response_model=PromptResponse, summary="更新人设")
async def update_prompt(
    prompt_id: str,
    request: PromptUpdateRequest,
    prompt_service: PromptService = Depends(get_service(PromptService))
) -> PromptResponse:
    """更新人设信息"""
    prompt = await prompt_service.update_prompt(
        prompt_id=prompt_id,
        prompt=request.prompt,
        title=request.title,
        state=request.state
    )
    if not prompt:
        raise HTTPException(status_code=404, detail="人设不存在")
    return PromptResponse.from_do(prompt)


@router.delete("/{prompt_id}", summary="删除人设")
async def delete_prompt(
    prompt_id: str,
    prompt_service: PromptService = Depends(get_service(PromptService))
) -> dict:
    """删除人设（软删除）"""
    success = await prompt_service.delete_prompt(prompt_id)
    if not success:
        raise HTTPException(status_code=404, detail="人设不存在")
    return {"success": True, "message": "删除成功"}


@router.delete("/{prompt_id}/hard", summary="彻底删除人设")
async def hard_delete_prompt(
    prompt_id: str,
    prompt_service: PromptService = Depends(get_service(PromptService))
) -> dict:
    """彻底删除人设（不可恢复）"""
    success = await prompt_service.hard_delete_prompt(prompt_id)
    if not success:
        raise HTTPException(status_code=404, detail="人设不存在")
    return {"success": True, "message": "已彻底删除"}