from http.client import HTTPException

from fastapi import APIRouter, Depends, Path
from pydantic import Field

from models.vo.base import Result, BaseResp, BaseReq
from services import UserService, get_service, get_app_user

router = APIRouter()


class UpdatePromptRequest(BaseReq):
    """更新人设请求模型"""
    user_id: str = Field("", description="用户id")
    prompt: str = Field(..., description="人设内容")
    title: str = Field(..., description="人设标题")


class PromptResponse(BaseResp):
    """人设响应模型"""
    user_id: str
    prompt: str
    title: str
    state: str


@router.put("/revise/prompt",summary="修改")
async def update_user_prompt(
    request: UpdatePromptRequest,
    user_service: UserService = Depends(get_service(UserService)),
    _=Depends(get_app_user)
):
    """
    根据用户ID修改user_prompt表中的人设字段

    - **user_id**: 用户唯一标识
    - **prompt**: 新的人设内容
    """
    await user_service.update_user_prompt(
        user_id=request.user_id,
        prompt=request.prompt
    )
    return Result.success_(msg="更新成功")


@router.get("/prompt/{user_id}", summary="获取用户人设")
async def get_user_prompt(
        user_id: str,
        user_service: UserService = Depends(get_service(UserService)),
        _=Depends(get_app_user)
):
    """根据用户ID获取用户人设"""
    user_prompt = await user_service.get_user_prompt(user_id)
    if not user_prompt:
        return Result.error_("未找到用户人设")
    return Result.success_(PromptResponse.from_do(user_prompt))


@router.post("/prompt", summary="创建用户人设")
async def create_user_prompt(
        request: UpdatePromptRequest,
        user_service: UserService = Depends(get_service(UserService)),
        _=Depends(get_app_user)
):
    """创建新的用户人设"""
    await user_service.create_user_prompt(
        user_id=request.user_id,
        prompt=request.prompt,
        title=request.title
    )
    return Result.success_(msg="人设创建成功")


@router.delete("/prompt/{user_id}", summary="删除用户人设")
async def delete_user_prompt(
    user_id: str = Path(..., description="用户唯一标识"),
    user_service: UserService = Depends(get_service(UserService)),
    userinfo=Depends(get_app_user)
):
    """删除用户人设"""
    success = await user_service.delete_user_prompt(user_id)
    if not success:
        return Result.error_("未找到用户人设")
    return Result.success_(msg="删除成功")
