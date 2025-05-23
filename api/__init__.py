from fastapi import APIRouter

from api import plugin, file

api_router = APIRouter()

api_router.include_router(plugin.router, prefix="/plugin", tags=["plugin"])
api_router.include_router(file.router, prefix="/file", tags=["file"])
