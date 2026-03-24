from datetime import datetime
from uuid import UUID

from app.schemas.base import BaseSchema, TimestampSchema


class GoalCreate(BaseSchema):
    title: str
    target_value: int
    deadline: datetime


class GoalUpdate(BaseSchema):
    title: str | None = None
    target_value: int | None = None
    current_value: int | None = None
    status: str | None = None
    deadline: datetime | None = None


class GoalResponse(TimestampSchema):
    id: UUID
    user_id: UUID
    title: str
    target_value: int
    current_value: int
    status: str
    deadline: datetime | None

    class Config:
        from_attributes = True
