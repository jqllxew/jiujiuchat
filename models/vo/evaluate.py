from datetime import datetime

from pydantic import BaseModel, Field
from typing import List, Optional

from models.vo.base import BaseReq, BaseResp


class EvaluateCreateRequest(BaseReq):
    """创建评估记录请求模型"""
    question_groups: str = Field(..., description="问题组")
    question: str = Field(..., description="问题内容")
    question_content :str =Field(...,description="问题详细内容")
    answer: List[str] = Field(..., description="答案列表")


class EvaluateUpdateRequest(BaseReq):
    """更新评估记录请求模型"""
    question_groups: Optional[str] = None
    question: Optional[str] = None
    question_content: Optional[str] = None
    answer: Optional[List[str]] = None


class EvaluateResponse(BaseResp):
    """评估记录响应模型"""
    id: str
    question_groups: str
    question: str
    question_content: str
    answer: List[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class EvaluateListResponse(BaseResp):
    """评估记录列表响应模型"""
    total: int
    items: List[EvaluateResponse]


class EvaluateSearchRequest(BaseReq):
    """搜索评估记录请求模型"""
    question_keyword: Optional[str] = None
    groups_keyword: Optional[str] = None
    question_content: Optional[str] = None