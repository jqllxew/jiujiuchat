
from fastapi import Request
from fastapi.exceptions import RequestValidationError
from starlette.responses import JSONResponse
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_422_UNPROCESSABLE_ENTITY, HTTP_500_INTERNAL_SERVER_ERROR


class ServiceException(Exception):
    def __init__(self, msg: str, code: int | None = None) -> None:
        self.msg = msg
        self.code = code

    def __str__(self) -> str:
        return self.msg


async def validation_exception_handler(req: Request, exc: Exception):
    if isinstance(exc, RequestValidationError):
        errors = exc.errors()
        custom_errors = []
        for err in errors:
            # loc = err["loc"][1] if len(err["loc"]) > 1 else None
            msg = err["msg"]
            custom_errors.append(msg.replace("Value error, ", ""))
        return JSONResponse(
            status_code=HTTP_400_BAD_REQUEST,
            content={"msg": custom_errors},
        )
    return await global_exception_handler(req, exc)


async def service_exception_handler(req: Request, exc: Exception):
    if isinstance(exc, ServiceException):
        return JSONResponse(
            status_code=HTTP_422_UNPROCESSABLE_ENTITY if exc.code is None else exc.code,
            content={
                "msg": [f"{str(exc)}"],
            },
        )
    return await global_exception_handler(req, exc)


async def global_exception_handler(_: Request, exc: Exception):
    return JSONResponse(
        status_code=HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "msg": [f"服务器内部错误: {str(exc)}"],
        },
    )
