from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import AlreadyExistsError, NotFoundError
from app.repositories import study_plan_repo, topic_repo
from app.schemas.study_plan import StudyPlanCreate, StudyPlanUpdate


class StudyPlanService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, user_id: UUID, data: StudyPlanCreate):
        # Check topic ownership
        topic = await topic_repo.get_by_id(self.db, data.topic_id, user_id)
        if not topic:
            raise NotFoundError(message="Topic not found")

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

    async def get_by_id(self, plan_id: UUID, user_id: UUID):
        plan = await study_plan_repo.get_by_id(self.db, plan_id, user_id)
        if not plan:
            raise NotFoundError("Study plan not found")
        return plan

    async def get_all(self, user_id: UUID):
        return await study_plan_repo.get_multi(self.db, user_id)

    async def update(self, plan_id: UUID, user_id: UUID, data: StudyPlanUpdate):
        plan = await self.get_by_id(plan_id, user_id)
        update_data = data.model_dump(exclude_unset=True, exclude_none=True)
        if not update_data:
            return plan

        # Check topic ownership if topic_id is being updated
        if "topic_id" in update_data:
            topic = await topic_repo.get_by_id(self.db, update_data["topic_id"], user_id)
            if not topic:
                raise NotFoundError("Topic not found")

        # Check for conflicts if time-related fields are updated
        if any(key in update_data for key in ["date", "start_time", "end_time"]):
            date = update_data.get("date", plan.date)
            start_time = update_data.get("start_time", plan.start_time)
            end_time = update_data.get("end_time", plan.end_time)

            conflict = await study_plan_repo.get_conflict(
                self.db,
                user_id=user_id,
                date=date,
                start_time=start_time,
                end_time=end_time,
            )
            if conflict and conflict.id != plan.id:
                raise AlreadyExistsError(message="Time slot conflict")

        return await study_plan_repo.update(self.db, plan=plan, data=update_data)

    async def delete(self, plan_id: UUID, user_id: UUID):
        plan = await study_plan_repo.delete(self.db, plan_id, user_id)
        if not plan:
            raise NotFoundError(message="Study plan not found")
        return plan
