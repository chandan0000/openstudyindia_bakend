from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.study_plan import StudyPlan


async def get_by_id(db: AsyncSession, plan_id: UUID, user_id: UUID) -> StudyPlan | None:
    result = await db.execute(
        select(StudyPlan).where(
            StudyPlan.id == plan_id,
            StudyPlan.user_id == user_id,
        )
    )
    return result.scalar_one_or_none()


async def create(db: AsyncSession, *, data: dict) -> StudyPlan:
    plan = StudyPlan(**data)
    db.add(plan)
    await db.flush()
    await db.refresh(plan)
    return plan


async def get_multi(db: AsyncSession, user_id: UUID):
    result = await db.execute(select(StudyPlan).where(StudyPlan.user_id == user_id))
    return list(result.scalars().all())


async def get_conflict(
    db: AsyncSession,
    *,
    user_id: UUID,
    date,
    start_time,
    end_time,
):
    result = await db.execute(
        select(StudyPlan).where(
            StudyPlan.user_id == user_id,
            StudyPlan.date == date,
            StudyPlan.start_time < end_time,
            StudyPlan.end_time > start_time,
        )
    )
    return result.scalar_one_or_none()


async def update(db: AsyncSession, *, plan: StudyPlan, data: dict) -> StudyPlan:
    for key, value in data.items():
        setattr(plan, key, value)
    await db.flush()
    await db.refresh(plan)
    return plan


async def delete(db: AsyncSession, plan_id: UUID, user_id: UUID) -> StudyPlan | None:
    plan = await get_by_id(db, plan_id, user_id)
    if plan:
        await db.delete(plan)
        await db.flush()
    return plan
