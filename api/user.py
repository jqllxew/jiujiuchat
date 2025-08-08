from http.client import HTTPException

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from services import UserService, get_service

router = APIRouter()


class UpdatePromptRequest(BaseModel):
    """更新人设请求模型"""
    user_id: str
    prompt: str
    title:str


class UpdatePromptResponse(BaseModel):
    """更新人设响应模型"""
    success: bool
    message: str
    data: dict

class PromptResponse(BaseModel):
    """人设响应模型"""
    user_id: str
    prompt: str
    title: str
    created_at: str
    updated_at: str
    state :str


@router.put("/Revise/prompt",summary="修改")
async def update_user_prompt(
    request: UpdatePromptRequest,
    user_service: UserService = Depends(get_service(UserService))
    # _=Depends(get_lobe_user)
) -> UpdatePromptResponse:
    """
    根据用户ID修改user_prompt表中的人设字段

    - **user_id**: 用户唯一标识
    - **prompt**: 新的人设内容
    """
    try:
        user_prompt = await user_service.update_user_prompt(
            user_id=request.user_id,
            prompt=request.prompt
        )

        return UpdatePromptResponse(
            success=True,
            message="人设更新成功",
            data={
                "user_id": user_prompt.user_id,
                "prompt": user_prompt.prompt,
                "updated_at": user_prompt.updated_at.isoformat()
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"更新失败: {str(e)}")


@router.get("/prompt/{user_id}", response_model=PromptResponse, summary="获取用户人设")
async def get_user_prompt(
        user_id: str,
        user_service: UserService = Depends(get_service(UserService))
        # _=Depends(get_lobe_user)
):
    """根据用户ID获取用户人设"""
    user_prompt = await user_service.get_user_prompt(user_id)

    if not user_prompt:
        raise HTTPException(status_code=404, detail="未找到用户人设")

    return PromptResponse(
        user_id=user_prompt.user_id,
        prompt=user_prompt.prompt,
        title=user_prompt.title,
        created_at=user_prompt.created_at.isoformat(),
        updated_at=user_prompt.updated_at.isoformat(),
        state=user_prompt.state
    )


@router.post("/prompt", summary="创建用户人设")
async def create_user_prompt(
        request: UpdatePromptRequest,
        user_service: UserService = Depends(get_service(UserService))
        # _=Depends(get_lobe_user)
) -> UpdatePromptResponse:
    """创建新的用户人设"""
    try:
        user_prompt = await user_service.create_user_prompt(
            user_id=request.user_id,
            prompt=request.prompt,
            title=request.title
        )

        return UpdatePromptResponse(
            success=True,
            message="人设创建成功",
            data={
                "user_id": user_prompt.user_id,
                "prompt": user_prompt.prompt,
                "title": user_prompt.title,
                "created_at": user_prompt.created_at.isoformat()
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"创建失败: {str(e)}")


@router.delete("/prompt/{user_id}", summary="删除用户人设")
async def delete_user_prompt(
        user_id: str,
        user_service: UserService = Depends(get_service(UserService))
        # _=Depends(get_lobe_user)
) -> dict:
    """删除用户人设"""
    success = await user_service.delete_user_prompt(user_id)
    if not success:
        raise HTTPException(status_code=404, detail="未找到用户人设")

    return {"success": True, "message": "删除成功"}