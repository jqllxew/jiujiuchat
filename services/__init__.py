import hashlib
import logging
from typing import Type, TypeVar, Callable

from fastapi import Depends, Request, Header
from jose import jwt
from starlette.status import HTTP_401_UNAUTHORIZED

from config import configs
from config.exc import ServiceException
from db import get_db, get_redis
from .base import BaseService
from .evaluate import EvaluateService
from .prompt import PromptService
from .qw import TokenService
from .user import UserService

T = TypeVar('T', bound=BaseService)


def get_service(cls: Type[T], ) -> Callable[..., T]:
    def wrapper(db=Depends(get_db), redis=Depends(get_redis)) -> T:
        return cls(db, redis)
    return wrapper


def _get_userinfo(req: Request, token: str) -> dict:
    if not token:
        raise ServiceException("token 不存在", HTTP_401_UNAUTHORIZED)
    hashed_key = hashlib.sha256(configs.JWT_SECRET_KEY.encode('utf-8')).digest()
    try:
        userinfo = jwt.decode(token, hashed_key, algorithms="HS256")  # type: ignore
        logging.info("url: %s, user_info: %s", req.url.path, userinfo)
        return userinfo
    except jwt.ExpiredSignatureError:
        raise ServiceException("token 已过期", HTTP_401_UNAUTHORIZED)
    except jwt.JWTError:
        raise ServiceException("token 非法", HTTP_401_UNAUTHORIZED)


# lobe-chat 测试端身份校验
def get_lobe_user(req: Request, token: str = Header("", alias="X-lobe-chat-auth")) -> dict:
    return _get_userinfo(req, token)


# app 端身份校验
def get_app_user(req: Request, token: str = Header("", alias="X-app-auth")) -> dict:
    return _get_userinfo(req, token)


# 管理端身份校验
def get_system_user(req: Request, token: str = Header("", alias="X-system-auth")) -> dict:
    return _get_userinfo(req, token)


__all__ = [
    "get_lobe_user",
    "get_app_user",
    "get_system_user",
    "get_service",
    "BaseService",
    "TokenService",
    "UserService",
    "PromptService",
    "EvaluateService",
]