from datetime import datetime
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import NotFoundError
from app.repositories import exam as repo


class ExamService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, user_id: UUID, data):
        return await repo.create(
            self.db,
            data={
                "user_id": user_id,
                "name": data.name,
                "exam_date": data.exam_date,
            },
        )

    async def get_all(self, user_id: UUID):
        exams = await repo.get_multi(self.db, user_id)

        # 🔥 add countdown
        now = datetime.utcnow()
        result = []
        for exam in exams:
            days_left = (exam.exam_date - now).days
            result.append(
                {
                    **exam.__dict__,
                    "days_left": days_left,
                }
            )

        return result

    async def delete(self, exam_id: UUID):
        exam = await repo.delete(self.db, exam_id)
        if not exam:
            raise NotFoundError(message="Exam not found")
        return exam
