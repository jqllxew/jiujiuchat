import random
import string

from captcha.image import ImageCaptcha
from fastapi import APIRouter, Depends, Response, Query
from redis.asyncio import Redis

from api.component.auth import get_app_user
from db import get_redis
from models.do import SuperDO
from models.vo import RegisterVO
from models.vo.login import LoginVO
from services import get_service
from services.login import LoginService

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
    captcha_id = str(SuperDO.generate_id())
    image = ImageCaptcha(width=width, height=height)
    data = image.generate(code)
    await redis.setex(f"captcha:{captcha_id}", 180, code)
    return Response(
        content=data.read(),
        media_type="image/png",
        headers={"X-Captcha-Id": captcha_id}
    )


@router.post("/register", summary="注册")
async def register(
    *,
    register_vo: RegisterVO,
    login_service: LoginService = Depends(get_service(LoginService)),
):
    user = await login_service.register(register_vo)
    return user


@router.post("/login", summary="登录")
async def login(
    *,
    login_vo: LoginVO,
    login_service: LoginService = Depends(get_service(LoginService))
):
    jwt_token = await login_service.login(login_vo)
    return jwt_token


@router.get("/session", summary="获取登录用户")
async def session(
    *,
    user=Depends(get_app_user)
):
    return user
