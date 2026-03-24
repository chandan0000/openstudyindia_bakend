from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class SessionStart(BaseModel):
    topic_id: UUID


class SessionResponse(BaseModel):
    id: UUID
    topic_id: UUID
    start_time: datetime
    end_time: datetime | None
    duration_minutes: int | None

    class Config:
        from_attributes = True
