import hashlib
import logging

from fastapi import Header, status, HTTPException, Request
from jose import jwt
from config import configs


def get_lobe_user(req: Request, token: str = Header("", alias="X-lobe-chat-auth")) -> dict:
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="token 不存在")
    hashed_key = hashlib.sha256(configs.JWT_SECRET_KEY.encode('utf-8')).digest()
    try:
        user_info = jwt.decode(token, hashed_key, algorithms="HS256")  # type: ignore
        logging.info("url: %s, user_info: %s", req.url.path, user_info)
        return user_info
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="token 已过期")
    except jwt.JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="token 非法")
