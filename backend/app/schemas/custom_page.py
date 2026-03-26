from collections.abc import Sequence
from typing import TypeVar

from fastapi_pagination import Page
from pydantic import ConfigDict, Field

T = TypeVar("T")


class CustomPage(Page[T]):
    """Custom pagination response that uses 'data' instead of 'items'"""

    items: Sequence[T] = Field(serialization_alias="data")

    model_config = ConfigDict(populate_by_name=True)
