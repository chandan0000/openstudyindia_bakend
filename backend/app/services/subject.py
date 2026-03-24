from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import AlreadyExistsError, NotFoundError
from app.repositories import subject_repo
from app.schemas.subject import SubjectCreate


class SubjectService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, user_id: UUID, data: SubjectCreate):
        existing = await subject_repo.get_by_name(self.db, user_id, data.name)
        if existing:
            raise AlreadyExistsError(message="Subject already exists")

        return await subject_repo.create(
            self.db,
            user_id=user_id,
            name=data.name,
        )

    async def get_all(self, user_id: UUID):
        return await subject_repo.get_multi(self.db, user_id)

    async def delete(self, subject_id: UUID):
        subject = await subject_repo.delete(self.db, subject_id)
        if not subject:
            raise NotFoundError(message="Subject not found")
        return subject
