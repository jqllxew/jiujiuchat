
import pydantic_core
from pydantic import BaseModel, model_validator, ValidationError


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
