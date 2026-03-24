from datetime import datetime
from uuid import UUID

from app.schemas.base import BaseSchema, TimestampSchema


class ExamCreate(BaseSchema):
    name: str
    exam_date: datetime


class ExamUpdate(BaseSchema):
    name: str | None = None
    exam_date: datetime | None = None


class ExamResponse(TimestampSchema):
    id: UUID
    user_id: UUID
    name: str
    exam_date: datetime
    days_left: int

    class Config:
        from_attributes = True
