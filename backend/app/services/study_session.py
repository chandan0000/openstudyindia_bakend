from datetime import UTC, datetime
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import AlreadyExistsError, NotFoundError
from app.repositories import study_session as repo
from app.repositories import topic_repo
from app.schemas.study_session import SessionStart, SessionUpdate


class StudySessionService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def start(self, user_id: UUID, data: SessionStart):
        # Check topic ownership
        topic = await topic_repo.get_by_id(self.db, data.topic_id, user_id)
        if not topic:
            raise NotFoundError(message="Topic not found")

        # Check already active session
        active = await repo.get_active_session(self.db, user_id)
        if active:
            raise AlreadyExistsError(message="Session already active")

        return await repo.create(
            self.db,
            user_id=user_id,
            topic_id=data.topic_id,
            start_time=datetime.now(UTC),
        )

    async def get_by_id(self, session_id: UUID, user_id: UUID):
        session = await repo.get_by_id(self.db, session_id, user_id)
        if not session:
            raise NotFoundError("Study session not found")
        return session

    async def end(self, user_id: UUID):
        session = await repo.get_active_session(self.db, user_id)
        if not session:
            raise NotFoundError(message="No active session")

        end_time = datetime.now(UTC)

        # Duration calculation
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

    async def update(self, session_id: UUID, user_id: UUID, data: SessionUpdate):
        session = await self.get_by_id(session_id, user_id)
        update_data = data.model_dump(exclude_unset=True, exclude_none=True)
        if not update_data:
            return session

        # Check topic ownership if topic_id is being updated
        if "topic_id" in update_data:
            topic = await topic_repo.get_by_id(self.db, update_data["topic_id"], user_id)
            if not topic:
                raise NotFoundError("Topic not found")

        return await repo.update(self.db, session, update_data)

    async def delete(self, session_id: UUID, user_id: UUID):
        session = await repo.delete(self.db, session_id, user_id)
        if not session:
            raise NotFoundError(message="Study session not found")
        return session
