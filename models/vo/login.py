from pydantic import field_validator, Field, model_validator
from models.vo.base import BaseReq


class RegisterVO(BaseReq):
    phone: str = Field(..., description="手机号")
    passwd: str = Field(..., description="密码")
    passwd_confirm: str = Field(..., description="确认密码")
    captcha_id: str = Field(..., description="返回的验证码id")
    captcha_code: str = Field(..., description="验证码")

    @field_validator("phone")
    def validate_phone(cls, v):
        import re
        if not re.match(r'^1[3-9]\d{9}$', v):
            raise ValueError("请输入正确的手机号")
        return v

    @model_validator(mode="after")
    def validate_fields(self):
        if self.passwd != self.passwd_confirm:
            raise ValueError("两次输入的密码不一致")
        return self


class LoginVO(BaseReq):
    phone: str = Field(..., description="手机号")
    passwd: str = Field(..., description="密码")
    captcha_id: str = Field(..., description="返回的验证码id")
    captcha_code: str = Field(..., description="验证码")
