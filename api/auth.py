import hashlib
import logging

from fastapi import Header, status, HTTPException, Request
from jose import jwt
from config import configs


def get_current_user(req: Request, token: str = Header("", alias="X-lobe-chat-auth")) -> dict:
    logging.info("headers: %s", req.headers)
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="token 不存在")
    hashed_key = hashlib.sha256(configs.JWT_SECRET_KEY.encode('utf-8')).digest()
    try:
        return jwt.decode(token, hashed_key, algorithms="HS256")  # type: ignore
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="token 已过期")
    except jwt.JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="token 非法")
