from typing import Type, TypeVar, Callable

from fastapi import Depends

from db import get_db, get_redis
from .base import BaseService
from .qw import TokenService
from .user import UserService

T = TypeVar('T', bound=BaseService)


def get_service(cls: Type[T], ) -> Callable[..., T]:
    def wrapper(db=Depends(get_db), redis=Depends(get_redis)) -> T:
        return cls(db, redis)
    return wrapper


__all__ = [
    "get_service",
    "BaseService",
    "TokenService",
    "UserService"
]