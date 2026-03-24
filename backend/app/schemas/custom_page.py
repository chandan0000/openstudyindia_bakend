from typing import Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class CustomPage(BaseModel, Generic[T]):
    data: list[T]
    total: int
    page: int
    size: int
    pages: int
