import random
import string
from typing import Any

from captcha.image import ImageCaptcha
from fastapi import APIRouter, Depends, Response, Query
from redis.asyncio import Redis
from starlette import status
from starlette.exceptions import HTTPException

from db import get_redis
from models.do import TimestampMixin
from models.vo import RegisterVO
import pydantic

router = APIRouter()


def generate_code(length=4):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))


@router.get("/captcha", summary="验证码")
async def get_captcha(
    *,
    redis: Redis = Depends(get_redis),
    width: int = Query(160, ge=120, description="宽度"),
    height: int = Query(60, ge=50, description="高度"),
):
    code = generate_code()
    captcha_id = str(TimestampMixin.generate_id())
    image = ImageCaptcha(width=width, height=height)
    data = image.generate(code)
    await redis.setex(f"captcha:{captcha_id}", 180, code)
    return Response(
        content=data.read(),
        media_type="image/png",
        headers={"X-Captcha-Id": captcha_id}
    )


@router.post("/register", summary="注册")
async def register(register_vo: RegisterVO):
    # raise ValueError("测试")
    return register_vo


@router.post("/login", summary="登录")
async def login(
    *,
    phone: str,
    passwd: str
) -> Any:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
