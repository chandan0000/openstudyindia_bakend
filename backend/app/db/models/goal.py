import uuid
from datetime import datetime

from sqlalchemy import UUID, DateTime, ForeignKey, String, text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, TimestampMixin


class Goal(Base, TimestampMixin):
    __tablename__ = "goals"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, server_default=text("uuidv7()")
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )

    title: Mapped[str] = mapped_column(String(255))

    current_value: Mapped[int] = mapped_column(default=0)

    status: Mapped[str] = mapped_column(String(50), default="pending")

    deadline: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
