from fastapi import APIRouter, Depends, Response, Query

from models.vo.base import Result
from models.vo.login import LoginVO, LoginByPasswordVO
from services import get_service, get_app_user, get_system_user
from services.login import LoginService

router = APIRouter()


@router.get("/captcha", summary="图形验证码")
async def get_captcha(
    *,
    width: int = Query(160, ge=120, description="宽度"),
    height: int = Query(60, ge=50, description="高度"),
    login_service: LoginService = Depends(get_service(LoginService)),
):
    captcha_id, data = await login_service.get_captcha_img(width, height)
    return Response(
        content=data,
        media_type="image/png",
        headers={"X-Captcha-Id": captcha_id}
    )


@router.get("/captcha-sms", summary="短信验证码")
async def get_captcha_sms(
    *,
    phone: str = Query(..., pattern=r"^1[3-9]\d{9}$", description="手机号"),
    login_service: LoginService = Depends(get_service(LoginService))
):
    await login_service.get_captcha_sms(phone)
    return Result.success_(msg="短信验证码已发送")


@router.post("/login", summary="注册/登录(app)", description="如果用户不存在则注册")
async def login(
    *,
    login_vo: LoginVO,
    login_service: LoginService = Depends(get_service(LoginService))
):
    jwt_token = await login_service.login(login_vo)
    return Result.success_(jwt_token)


@router.post("/login-system", summary="登录(system)")
async def login_by_password(
    *,
    login_vo: LoginByPasswordVO,
    login_service: LoginService = Depends(get_service(LoginService))
):
    jwt_token = await login_service.login_by_password(login_vo)
    return Result.success_(jwt_token)


@router.get("/session", summary="获取登录用户(app)")
async def session(
    *,
    user=Depends(get_app_user)
):
    return Result.success_(user)


@router.get("/session-system", summary="获取系统用户")
async def get_system_user(
    *,
    user=Depends(get_system_user)
):
    return user

# @router.get("/", summary="登出")
# async def logout(
#     *,
#     login_service: LoginService = Depends(get_service(LoginService))
# ):
#
#     await login_service.logout()
#     return Result.success_(msg="已登出")
