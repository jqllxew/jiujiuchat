import hashlib
import logging

from fastapi import Header, status, HTTPException, Request
from jose import jwt
from config import configs


def _get_userinfo(req: Request, token: str) -> dict:
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="token 不存在")
    hashed_key = hashlib.sha256(configs.JWT_SECRET_KEY.encode('utf-8')).digest()
    try:
        userinfo = jwt.decode(token, hashed_key, algorithms="HS256")  # type: ignore
        logging.info("url: %s, user_info: %s", req.url.path, userinfo)
        return userinfo
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="token 已过期")
    except jwt.JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="token 非法")


# lobe-chat 测试端身份校验
def get_lobe_user(req: Request, token: str = Header("", alias="X-lobe-chat-auth")) -> dict:
    return _get_userinfo(req, token)


# app 端身份校验
def get_app_user(req: Request, token: str = Header("", alias="X-app-auth")) -> dict:
    return _get_userinfo(req, token)


# 管理端身份校验
def get_system_user(req: Request, token: str = Header("", alias="X-system-auth")) -> dict:
    return _get_userinfo(req, token)
