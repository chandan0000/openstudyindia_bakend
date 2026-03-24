from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import NotFoundError
from app.repositories import exam as repo
from app.schemas.exam import ExamCreate, ExamUpdate


class ExamService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, user_id: UUID, data: ExamCreate):
        return await repo.create(
            self.db,
            data={
                "user_id": user_id,
                "name": data.name,
                "exam_date": data.exam_date,
            },
        )

    async def get_by_id(self, exam_id: UUID, user_id: UUID):
        exam = await repo.get_by_id(self.db, exam_id, user_id)
        if not exam:
            raise NotFoundError("Exam not found")
        return exam

    async def get_all(self, user_id: UUID):
        return await repo.get_multi(self.db, user_id)

    async def update(self, exam_id: UUID, user_id: UUID, data: ExamUpdate):
        exam = await self.get_by_id(exam_id, user_id)
        update_data = data.model_dump(exclude_unset=True, exclude_none=True)
        if not update_data:
            return exam
        return await repo.update(self.db, exam=exam, data=update_data)

    async def delete(self, exam_id: UUID, user_id: UUID):
        exam = await repo.delete(self.db, exam_id, user_id)
        if not exam:
            raise NotFoundError(message="Exam not found")
        return exam
