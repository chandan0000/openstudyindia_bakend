from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import AlreadyExistsError, NotFoundError
from app.repositories import study_plan_repo


class StudyPlanService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, user_id: UUID, data):
        conflict = await study_plan_repo.get_conflict(
            self.db,
            user_id=user_id,
            date=data.date,
            start_time=data.start_time,
            end_time=data.end_time,
        )

        if conflict:
            raise AlreadyExistsError(message="Time slot conflict")

        return await study_plan_repo.create(
            self.db,
            data={
                "user_id": user_id,
                "topic_id": data.topic_id,
                "date": data.date,
                "start_time": data.start_time,
                "end_time": data.end_time,
            },
        )

    async def get_all(self, user_id: UUID):
        return await study_plan_repo.get_multi(self.db, user_id)

    async def delete(self, plan_id: UUID):
        plan = await study_plan_repo.delete(self.db, plan_id)
        if not plan:
            raise NotFoundError(message="Study plan not found")
        return plan
