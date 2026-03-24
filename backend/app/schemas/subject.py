from uuid import UUID

from app.schemas.base import BaseSchema


class SubjectCreate(BaseSchema):
    name: str


class SubjectResponse(BaseSchema):
    id: UUID
    name: str

    class Config:
        from_attributes = True
