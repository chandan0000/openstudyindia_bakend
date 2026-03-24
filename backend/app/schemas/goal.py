from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class GoalCreate(BaseModel):
    title: str
    target_value: int
    deadline: datetime


class GoalUpdate(BaseModel):
    title: str | None = None
    target_value: int | None = None
    current_value: int | None = None
    status: str | None = None


class GoalResponse(BaseModel):
    id: UUID
    title: str
    target_value: int
    current_value: int
    status: str

    class Config:
        from_attributes = True
