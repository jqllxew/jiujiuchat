from fastapi import APIRouter

from api import plugin

api_router = APIRouter()

api_router.include_router(plugin.router, prefix="/plugin", tags=["plugin"])
