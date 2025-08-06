from fastapi import APIRouter, Request
from fastapi.exceptions import RequestValidationError
from starlette.responses import JSONResponse
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY, HTTP_500_INTERNAL_SERVER_ERROR

from api import plugin, file, callback, login

api_router = APIRouter()

api_router.include_router(plugin.router, prefix="/plugin", tags=["插件"])
api_router.include_router(file.router, prefix="/file", tags=["文件"])
api_router.include_router(callback.router, prefix="/callback", tags=["回调"])
api_router.include_router(login.router, prefix="/login", tags=["登录"])


async def validation_exception_handler(_: Request, exc: Exception):
    if isinstance(exc, RequestValidationError):
        errors = exc.errors()
        custom_errors = []
        for err in errors:
            # loc = err["loc"][1] if len(err["loc"]) > 1 else None
            msg = err['msg']
            custom_errors.append(msg.replace("Value error, ", ""))
        return JSONResponse(
            status_code=HTTP_422_UNPROCESSABLE_ENTITY,
            content={"msg": custom_errors},
        )


async def global_exception_handler(_: Request, exc: Exception):
    return JSONResponse(
        status_code=HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "msg": f"服务器内部错误: {str(exc)}",
        },
    )
