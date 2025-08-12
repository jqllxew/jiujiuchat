from pydantic import field_validator, Field
from models.vo.base import BaseReq


class RegisterVO(BaseReq):
    phone: str = Field(..., description="手机号")
    # passwd: str = Field(..., description="密码")
    code: str = Field(..., description="验证码")

    @field_validator("phone")
    def validate_phone(cls, v):
        import re
        if not re.match(r'^1[3-9]\d{9}$', v):
            raise ValueError("请输入正确的手机号")
        return v


class LoginVO(RegisterVO):
    ...


class LoginByPasswordVO(LoginVO):
    passwd: str = Field(..., description="密码")

    @field_validator("passwd")
    def validate_passwd(cls, v):
        if len(v) < 6 or len(v) > 20:
            raise ValueError("密码长度必须在6到20个字符之间")
        return v
