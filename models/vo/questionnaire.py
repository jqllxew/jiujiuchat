from datetime import datetime

from fastapi import Query
from pydantic import BaseModel, Field
from typing import List, Optional

from starlette.requests import Request

from models.vo.base import BaseReq, BaseResp


class QuestionnaireSaveReq(BaseReq):
    """保存问卷项请求模型"""
    id: Optional[str] = Field(None, description="问卷项id(不为空则为更新操作)")
    question_groups: str = Field(..., description="问题组")
    question: Optional[str] = Field(None, description="问题内容")
    question_content: Optional[str] = Field(None, description="问题详细内容")
    answer: List[str] = Field(..., description="答案列表")
    answer_extreme: Optional[List[str]] = Field(None, description="答案两端倾向")
    weights: Optional[list] = Field(None, description="维度权重")


class QuestionnaireAnswerReq(BaseReq):
    """回答问卷请求模型"""
    id: str = Field(..., description="问卷项id")
    answer: List[str] = Field(..., description="用户答案列表")


class QuestionnaireAnswersReq(BaseReq):
    user_id: str = Field(None, description="用户ID")
    answers: List[QuestionnaireAnswerReq] = Field(
        ..., description="用户回答的问卷列表"
    )


class QuestionnaireResponse(BaseResp):
    """评估记录响应模型"""
    id: str
    question_groups: str
    question: str
    question_content: str
    answer: List[str]


# class QuestionnaireListResponse(BaseResp):
#     """评估记录列表响应模型"""
#     total: int
#     items: List[QuestionnaireResponse]


class QuestionnaireSearchRequest(BaseReq):
    """搜索评估记录请求模型"""
    page: int = Field(..., ge=1, description="页数")
    limit: int = Field(10, ge=1, le=1000, description="每页数量")
    question_groups: Optional[str] = Field(None, description="问题组")
    question: Optional[str] = Field(None, description="问题内容")
    question_content: Optional[str] = Field(None, description="问题详细内容")
