import uuid
from datetime import datetime

from sqlalchemy import UUID, DateTime, ForeignKey, Index, text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, TimestampMixin


class StudyPlan(Base, TimestampMixin):
    __tablename__ = "study_plans"

    id: Mapped[int] = mapped_column(
        UUID(as_uuid=True), primary_key=True, server_default=text("uuidv7()")
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    topic_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("topics.id", ondelete="CASCADE"), nullable=False
    )
    start_time = mapped_column(DateTime(timezone=True))
    end_time = mapped_column(DateTime(timezone=True))
    date: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    __table_args__ = (Index("idx_study_plans_user_date", "user_id", "date"),)
