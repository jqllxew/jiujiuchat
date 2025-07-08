from typing import Type, TypeVar, Callable

from fastapi import Depends

from db import get_db
from services.base import BaseService
from services.qw import TokenService

T = TypeVar('T', bound=BaseService)


def get_service(cls: Type[T], ) -> Callable[..., T]:
    def wrapper(db=Depends(get_db)) -> T:
        return cls(db)
    return wrapper


__all__ = [
    "get_service",
    "BaseService",
    "TokenService"
]