from pydantic import field_validator, Field
from models.vo.base import BaseReq


class RegisterVO(BaseReq):
    phone: str = Field(..., description="手机号")
    passwd: str = Field(..., description="密码")
    captcha: str = Field(..., description="验证码")

    @field_validator("phone")
    def validate_phone(cls, v):
        import re
        if not re.match(r'^1[3-9]\d{9}$', v):
            raise ValueError("请输入正确的手机号")
        return v
