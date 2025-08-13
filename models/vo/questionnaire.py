from typing import List, Optional

from pydantic import Field, field_validator

from models.vo.base import BaseReq, BaseResp
from models.enum import Dimensional


class QuestionnaireSaveReq(BaseReq):
    """保存问卷项请求模型"""
    id: Optional[str] = Field(None, description="问卷项id(不为空则为更新操作)")
    group_name: str = Field(..., description="问题组名称(若不存在则创建)")
    question: Optional[str] = Field(None, description="问题内容")
    question_content: Optional[str] = Field(None, description="问题详细内容")
    answer: List[str] = Field(..., description="答案列表")
    answer_extreme: Optional[List[str]] = Field(None, description="答案两端倾向")
    weights: Optional[dict] = Field(None, description="维度权重")
    sort: Optional[int] = Field(None, description="排序")

    @field_validator("weights")
    def validate_weights(cls, v):
        if v is not None:
            if not isinstance(v, dict):
                raise ValueError("维度权重必须是json")
            # 检查维度权重中的 key为 Dimensional 枚举值, val 为浮点数 需保留1位小数
            values = [member.value for member in Dimensional.__members__.values()]
            for key in v.keys():
                if key not in values:
                    raise ValueError(f"维度权重中的key必须是 {values} 中的一个")
                if not isinstance(v[key], (int, float)):
                    raise ValueError(f"维度权重中的'{key}'的值必须是数字")
                v[key] = round(float(v[key]), 1)  # 保留1位小数
        return v


class QuestionnaireAnswerReq(BaseReq):
    """回答问卷请求模型"""
    id: str = Field(..., description="问卷项id")
    answer: List[str] = Field(..., description="用户答案列表")


class QuestionnaireAnswersReq(BaseReq):
    user_id: str = Field(None, description="用户ID")
    answers: List[QuestionnaireAnswerReq] = Field(
        ..., description="用户回答的问卷列表"
    )


class GroupResp(BaseResp):
    id: Optional[str] = None
    name: Optional[str] = None
    weights: Optional[dict] = None
    sort: Optional[int] = None


class QuestionnaireResponse(BaseResp):
    id: Optional[str] = None
    group_id: Optional[str] = None
    group_name: Optional[str] = None
    question: Optional[str] = None
    question_content: Optional[str] = None
    answer: Optional[list] = None


# class QuestionnaireListResponse(BaseResp):
#     """评估记录列表响应模型"""
#     total: int
#     items: List[QuestionnaireResponse]


class QuestionnaireSearchRequest(BaseReq):
    """搜索评估记录请求模型"""
    page: int = Field(..., ge=1, description="页数")
    limit: int = Field(10, ge=1, le=1000, description="每页数量")
    group_name: Optional[str] = Field(None, description="问题组")
    question: Optional[str] = Field(None, description="问题内容")
    question_content: Optional[str] = Field(None, description="问题详细内容")
