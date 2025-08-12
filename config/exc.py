
from fastapi import Request
from fastapi.exceptions import RequestValidationError
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_422_UNPROCESSABLE_ENTITY, HTTP_500_INTERNAL_SERVER_ERROR

from models.vo.base import Result


class ServiceException(Exception):
    def __init__(self, msg: str, code: int | None = None) -> None:
        self.msg = msg
        self.code = code

    def __str__(self) -> str:
        return self.msg


ERROR_MESSAGES = {
    "greater_than_equal": "必须大于等于 {ge}",
    "less_than_equal": "必须小于等于 {le}",
    "min_length": "长度不能小于 {min_length}",
    "max_length": "长度不能大于 {max_length}",
    "type_parsing": "类型错误，期待 {expected_type}",
    "missing": "不能为空",
}


async def validation_exception_handler(req: Request, exc: Exception):
    if isinstance(exc, RequestValidationError):
        errors = exc.errors()
        custom_errors = []
        for err in errors:
            err_type = err.get("type")
            _loc = err.get("loc", [])
            loc = _loc[1] if len(_loc) > 1 else None
            msg = err.get("msg", "")
            if err_type and err_type in ERROR_MESSAGES:
                try:
                    msg = ERROR_MESSAGES[err_type].format(**err.get("ctx", {}))
                except:
                    pass
                custom_errors.append(f"{loc} {msg}")
            else:
                custom_errors.append(msg.replace("Value error, ", ""))
        return Result.error_(custom_errors, HTTP_400_BAD_REQUEST)
    return await global_exception_handler(req, exc)


async def service_exception_handler(req: Request, exc: Exception):
    if isinstance(exc, ServiceException):
        return Result.error_(f"{str(exc)}", HTTP_422_UNPROCESSABLE_ENTITY if exc.code is None else exc.code)
    return await global_exception_handler(req, exc)


async def global_exception_handler(_: Request, exc: Exception):
    return Result.error_(f"服务器内部错误: {str(exc)}", HTTP_500_INTERNAL_SERVER_ERROR)
