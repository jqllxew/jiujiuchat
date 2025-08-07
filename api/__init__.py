from fastapi import APIRouter
from api import plugin, file, callback, login

from api import plugin, file, callback, user

api_router = APIRouter()

api_router.include_router(plugin.router, prefix="/plugin", tags=["插件"])
api_router.include_router(file.router, prefix="/file", tags=["文件"])
api_router.include_router(callback.router, prefix="/callback", tags=["回调"])
api_router.include_router(login.router, prefix="/login", tags=["登录"])

api_router.include_router(user.router,prefix="/user" ,tags=["用户"])
