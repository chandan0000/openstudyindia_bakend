from uuid import UUID

from app.schemas.base import BaseSchema, TimestampSchema


class TopicCreate(BaseSchema):
    name: str
    subject_id: UUID


class TopicUpdate(BaseSchema):
    name: str | None = None
    subject_id: UUID | None = None


class TopicResponse(TimestampSchema):
    id: UUID
    name: str
    subject_id: UUID

    class Config:
        from_attributes = True
