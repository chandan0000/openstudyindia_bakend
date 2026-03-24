from datetime import date as DateType
from datetime import datetime
from uuid import UUID

from pydantic import field_validator

from app.schemas.base import BaseSchema, TimestampSchema


class StudyPlanCreate(BaseSchema):
    topic_id: UUID
    date: DateType
    start_time: datetime
    end_time: datetime

    @field_validator("end_time")
    def validate_time(cls, v, info):
        if v <= info.data["start_time"]:
            raise ValueError("end_time must be after start_time")
        return v


class StudyPlanUpdate(BaseSchema):
    topic_id: UUID | None = None
    date: DateType | None = None
    start_time: datetime | None = None
    end_time: datetime | None = None

    @field_validator("end_time")
    def validate_time(cls, v, info):
        if (
            "start_time" in info.data
            and v
            and info.data["start_time"]
            and v <= info.data["start_time"]
        ):
            raise ValueError("end_time must be after start_time")
        return v


class StudyPlanResponse(TimestampSchema):
    id: UUID
    user_id: UUID
    topic_id: UUID
    date: DateType
    start_time: datetime
    end_time: datetime

    class Config:
        from_attributes = True
