from uuid import UUID

from app.schemas.base import BaseSchema, TimestampSchema


class SubjectCreate(BaseSchema):
    name: str


class SubjectUpdate(BaseSchema):
    name: str | None = None


class SubjectResponse(TimestampSchema):
    id: UUID
    name: str
    user_id: UUID

    class Config:
        from_attributes = True
