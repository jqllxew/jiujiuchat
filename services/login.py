import hashlib
from datetime import timedelta, datetime

from jose import jwt
from sqlalchemy import select, func

from config import configs
from models.vo import RegisterVO
from models.do import User
from models.vo.login import LoginVO
from services.base import BaseService
from config.exc import ServiceException


def create_access_token(data: dict, expires_delta: timedelta = timedelta(hours=8)) -> str:
    to_encode = data.copy()
    expire = datetime.now() + expires_delta
    to_encode.update({"exp": expire})
    hashed_key = hashlib.sha256(configs.JWT_SECRET_KEY.encode("utf-8")).digest()
    encoded_jwt = jwt.encode(to_encode, hashed_key, algorithm="HS256")
    return encoded_jwt


class LoginService(BaseService):

    async def check_captcha(self, captcha_id: str, captcha_code: str) -> str:
        _id = f"captcha:{captcha_id}"
        code = await self.redis.getex(_id)
        if not code:
            raise ServiceException("验证码已过期")
        if code != captcha_code.upper():
            raise ServiceException("验证码输入错误")
        return _id

    async def register(self, vo: RegisterVO):
        # captcha_id = await self.check_captcha(vo.captcha_id, vo.captcha_code)
        count = await self.select_first(select(func.count()).select_from(User).where(
            User.phone.__eq__(vo.phone)
        ))
        if count:
            raise ServiceException(f"手机号{vo.phone}已存在")
        user_do = User.from_vo(vo)
        self.db.add(user_do)
        await self.db.commit()
        # await self.redis.delete(captcha_id)
        return user_do

    async def login(self, vo: LoginVO):
        # captcha_id = await self.check_captcha(vo.captcha_id, vo.captcha_code)
        user_do = await self.select_first(select(User).where(
            User.phone.__eq__(vo.phone)
            # & User.passwd.__eq__(vo.passwd)
        ))
        if not user_do:
            raise ServiceException("用户不存在")
        jwt_token = create_access_token({
            "id": user_do.id,
            "phone": user_do.phone,
            "nickname": user_do.nickname,
        })
        # await self.redis.delete(captcha_id)
        return jwt_token
