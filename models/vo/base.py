from datetime import datetime
from typing import TypeVar, Type, Any, Optional, Generic

from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel, model_validator
from starlette.responses import JSONResponse
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY

T = TypeVar("T", bound=BaseModel)
AnyT = TypeVar("AnyT")


class BaseReq(BaseModel):

    @staticmethod
    def is_empty(x) -> bool:
        return x is None or (isinstance(x, (str, list, tuple, dict, set)) and len(x) == 0)

    @model_validator(mode="before")
    def check_required(cls, values: dict):
        errors = []
        for field_name, model_field in cls.model_fields.items():
            value = values.get(field_name)
            description = model_field.description or field_name
            if model_field.is_required() and cls.is_empty(value):
                errors.append({
                    "loc": (field_name,),
                    # "type": pydantic_core.PydanticCustomError("value_error", f"{description}不能为空"),  # type: ignore
                    "input": value,
                    "msg": f"{description}不能为空"
                })
        if errors:
            raise RequestValidationError(errors)
        return values


class BaseResp(BaseModel):
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @classmethod
    def from_do(cls: Type[T], do_instance) -> T:
        do_dict = {c.key: getattr(do_instance, c.key) for c in do_instance.__table__.columns}
        vo_fields = set(cls.model_fields.keys())  # Pydantic v2+
        filtered = {k: v for k, v in do_dict.items() if k in vo_fields}
        return cls(**filtered)

    class Config:
        json_encoders = {
            datetime: lambda v: v.strftime("%Y-%m-%d %H:%M:%S") if v else None,
        }
        from_attributes = True


class Result(BaseModel, Generic[AnyT]):
    success: bool = True
    msg: Optional[list] = None
    data: Optional[AnyT] = None

    @classmethod
    def error_(cls, msg: str | list, status_code: int = HTTP_422_UNPROCESSABLE_ENTITY) -> JSONResponse:
        if isinstance(msg, str):
            msg = [msg]
        r = cls(success=False, msg=msg).model_dump()
        return JSONResponse(
            status_code=status_code,
            content=r
        )

    @classmethod
    def success_(cls, data=None, msg: Optional[str] = None) -> "Result":
        if isinstance(msg, str):
            msg = [msg]
        return cls(data=data, msg=msg)


class Page(BaseModel, Generic[AnyT]):
    total: int
    items: Optional[list[AnyT]]

    @classmethod
    def from_items(cls, items: list[Any], total: int) -> "Page":
        return cls(total=total, items=items)
