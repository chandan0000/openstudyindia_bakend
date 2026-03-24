from datetime import UTC, datetime
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import AlreadyExistsError, NotFoundError
from app.repositories import study_session as repo


class StudySessionService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def start(self, user_id: UUID, topic_id: UUID):
        # ❗ check already active session
        active = await repo.get_active_session(self.db, user_id)
        if active:
            raise AlreadyExistsError(message="Session already active")

        return await repo.create(
            self.db,
            user_id=user_id,
            topic_id=topic_id,
            start_time=datetime.now(UTC),
        )

    async def end(self, user_id: UUID):
        session = await repo.get_active_session(self.db, user_id)
        if not session:
            raise NotFoundError(message="No active session")

        end_time = datetime.now(UTC)

        # 🔥 duration calculation
        duration = int((end_time - session.start_time).total_seconds() / 60)

        return await repo.update(
            self.db,
            session,
            data={
                "end_time": end_time,
                "duration_minutes": duration,
            },
        )

    async def get_all(self, user_id: UUID):
        return await repo.get_multi(self.db, user_id)
