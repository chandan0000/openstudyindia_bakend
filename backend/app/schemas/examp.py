from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class ExamCreate(BaseModel):
    name: str
    exam_date: datetime


class ExamResponse(BaseModel):
    id: UUID
    name: str
    exam_date: datetime

    class Config:
        from_attributes = True
