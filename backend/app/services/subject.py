from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import AlreadyExistsError, NotFoundError
from app.repositories import subject_repo
from app.schemas.subject import SubjectCreate, SubjectUpdate


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

    async def get_by_id(self, subject_id: UUID, user_id: UUID):
        subject = await subject_repo.get_by_id(self.db, subject_id, user_id)
        if not subject:
            raise NotFoundError("Subject not found")
        return subject

    async def get_all(self, user_id: UUID):
        return await subject_repo.get_multi(self.db, user_id)

    async def update(self, subject_id: UUID, user_id: UUID, data: SubjectUpdate):
        subject = await self.get_by_id(subject_id, user_id)
        update_data = data.model_dump(exclude_unset=True, exclude_none=True)
        if not update_data:
            return subject
        return await subject_repo.update(self.db, subject=subject, data=update_data)

    async def delete(self, subject_id: UUID, user_id: UUID):
        subject = await subject_repo.delete(self.db, subject_id, user_id)
        if not subject:
            raise NotFoundError(message="Subject not found")
        return subject
