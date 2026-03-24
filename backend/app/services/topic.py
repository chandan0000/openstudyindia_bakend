from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import AlreadyExistsError, NotFoundError
from app.repositories import subject_repo, topic_repo
from app.schemas.topic import TopicCreate, TopicUpdate


class TopicService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, user_id: UUID, data: TopicCreate):
        # Check subject ownership
        subject = await subject_repo.get_by_id(self.db, data.subject_id, user_id)
        if not subject:
            raise NotFoundError(message="Subject not found")

        # Check duplicate
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

    async def get_by_id(self, topic_id: UUID, user_id: UUID):
        topic = await topic_repo.get_by_id(self.db, topic_id, user_id)
        if not topic:
            raise NotFoundError("Topic not found")
        return topic

    async def get_all(self, user_id: UUID, subject_id: UUID):
        # Check subject ownership
        subject = await subject_repo.get_by_id(self.db, subject_id, user_id)
        if not subject:
            raise NotFoundError(message="Subject not found")

        return await topic_repo.get_multi(self.db, subject_id)

    async def update(self, topic_id: UUID, user_id: UUID, data: TopicUpdate):
        topic = await self.get_by_id(topic_id, user_id)
        update_data = data.model_dump(exclude_unset=True, exclude_none=True)
        if not update_data:
            return topic

        # If subject_id is being updated, check ownership of new subject
        if "subject_id" in update_data:
            new_subject = await subject_repo.get_by_id(self.db, update_data["subject_id"], user_id)
            if not new_subject:
                raise NotFoundError("Subject not found")

        return await topic_repo.update(self.db, topic=topic, data=update_data)

    async def delete(self, topic_id: UUID, user_id: UUID):
        topic = await topic_repo.delete(self.db, topic_id, user_id)
        if not topic:
            raise NotFoundError(message="Topic not found")
        return topic
