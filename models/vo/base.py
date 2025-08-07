from datetime import datetime
from typing import TypeVar, Type

import pydantic_core
from pydantic import BaseModel, model_validator, ValidationError, field_serializer

T = TypeVar("T", bound=BaseModel)


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
            if not cls.is_empty(model_field.default) and cls.is_empty(value):
                errors.append({
                    "loc": (field_name, ),
                    "type": pydantic_core.PydanticCustomError("value_error", f"{description}不能为空"),  # type: ignore
                    "input": value
                })
        if errors:
            raise ValidationError.from_exception_data(cls, errors)
        return values


class BaseResp(BaseModel):
    @classmethod
    def from_do(cls: Type[T], do_instance) -> T:
        do_dict = {c.key: getattr(do_instance, c.key) for c in do_instance.__table__.columns}
        vo_fields = set(cls.model_fields.keys())  # Pydantic v2+
        filtered = {k: v for k, v in do_dict.items() if k in vo_fields}
        return cls(**filtered)

    class Config:
        json_encoders = {
            datetime: lambda v: v.strftime("%Y-%m-%d %H:%M:%S")
        }
