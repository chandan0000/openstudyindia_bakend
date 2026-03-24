from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import AlreadyExistsError, NotFoundError
from app.repositories import subject_repo, topic_repo
from app.schemas.topic import TopicCreate


class TopicService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, user_id: UUID, data: TopicCreate):
        # 🔥 Check subject exists (ownership check)
        subject = await subject_repo.get_by_id(self.db, data.subject_id)
        if not subject or subject.user_id != user_id:
            raise NotFoundError(message="Subject not found")

        # 🔥 duplicate check
        existing = await topic_repo.get_by_name(
            self.db,
            subject_id=data.subject_id,
            name=data.name,
        )
        if existing:
            raise AlreadyExistsError(message="Topic already exists")

        return await topic_repo.create(
            self.db,
            subject_id=data.subject_id,
            name=data.name,
        )

    async def get_all(self, user_id: UUID, subject_id: UUID):
        # 🔥 ownership check again
        subject = await subject_repo.get_by_id(self.db, subject_id)
        if not subject or subject.user_id != user_id:
            raise NotFoundError(message="Subject not found")

        return await topic_repo.get_multi(self.db, subject_id)

    async def delete(self, user_id: UUID, topic_id: UUID):
        topic = await topic_repo.get_by_id(self.db, topic_id)
        if not topic:
            raise NotFoundError(message="Topic not found")

        subject = await subject_repo.get_by_id(self.db, topic.subject_id)
        if not subject or subject.user_id != user_id:
            raise NotFoundError(message="Not allowed")

        await topic_repo.delete(self.db, topic_id)
        return topic
