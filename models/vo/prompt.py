from datetime import datetime

from models.vo.base import BaseReq, BaseResp
from typing import Optional


class PromptCreateRequest(BaseReq):
    """创建prompt请求模型"""
    prompt: str
    title: str
    # state: Optional[str] = "0"


class PromptResponse(BaseResp):
    """prompt响应模型"""
    id: str
    prompt: str
    title: str
    state: str
    created_at: datetime
    updated_at: datetime


class PromptUpdateRequest(BaseReq):
    """更新prompt请求模型"""
    prompt: Optional[str] = None
    title: Optional[str] = None
    # state: Optional[str] = None

class PromptListResponse(BaseResp):
    """prompt列表响应模型"""
    total: int
    items: list[PromptResponse]