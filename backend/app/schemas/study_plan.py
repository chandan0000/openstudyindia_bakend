from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel, field_validator


class StudyPlanCreate(BaseModel):
    topic_id: UUID
    date: date
    start_time: datetime
    end_time: datetime

    @field_validator("end_time")
    def validate_time(cls, v, info):
        if v <= info.data["start_time"]:
            raise ValueError("end_time must be after start_time")
        return v
