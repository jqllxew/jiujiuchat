from fastapi import APIRouter

from api import plugin, file, callback

api_router = APIRouter()

api_router.include_router(plugin.router, prefix="/plugin", tags=["plugin"])
api_router.include_router(file.router, prefix="/file", tags=["file"])
api_router.include_router(callback.router, prefix="/callback", tags=["callback"])
