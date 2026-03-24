from uuid import UUID

from app.schemas.base import BaseSchema


class TopicCreate(BaseSchema):
    name: str
    subject_id: UUID


class TopicResponse(BaseSchema):
    id: UUID
    name: str
    subject_id: UUID

    class Config:
        from_attributes = True
