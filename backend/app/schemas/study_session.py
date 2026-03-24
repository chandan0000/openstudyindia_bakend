from datetime import datetime
from uuid import UUID

from app.schemas.base import BaseSchema, TimestampSchema


class SessionStart(BaseSchema):
    topic_id: UUID


class SessionUpdate(BaseSchema):
    topic_id: UUID | None = None
    start_time: datetime | None = None
    end_time: datetime | None = None
    duration_minutes: int | None = None


class SessionResponse(TimestampSchema):
    id: UUID
    user_id: UUID
    topic_id: UUID
    start_time: datetime
    end_time: datetime | None = None
    duration_minutes: int | None = None

    class Config:
        from_attributes = True
