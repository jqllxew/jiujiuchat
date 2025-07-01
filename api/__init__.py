from fastapi import APIRouter

from api import plugin, file, callback

api_router = APIRouter()

api_router.include_router(plugin.router, prefix="/plugin", tags=["插件"])
api_router.include_router(file.router, prefix="/file", tags=["文件"])
api_router.include_router(callback.router, prefix="/callback", tags=["回调"])
