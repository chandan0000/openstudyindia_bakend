from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.goal import Goal


async def get_by_id(db: AsyncSession, goal_id: UUID, user_id: UUID) -> Goal | None:
    result = await db.execute(
        select(Goal).where(
            Goal.id == goal_id,
            Goal.user_id == user_id,
        )
    )
    return result.scalar_one_or_none()


async def get_multi(db: AsyncSession, user_id: UUID):
    result = await db.execute(select(Goal).where(Goal.user_id == user_id))
    return list(result.scalars().all())


async def create(db: AsyncSession, *, data: dict) -> Goal:
    goal = Goal(**data)
    db.add(goal)
    await db.flush()
    await db.refresh(goal)
    return goal


async def update(db: AsyncSession, goal: Goal, data: dict):
    for field, value in data.items():
        setattr(goal, field, value)

    db.add(goal)
    await db.flush()
    await db.refresh(goal)
    return goal


async def delete(db: AsyncSession, goal_id: UUID, user_id: UUID) -> Goal | None:
    goal = await get_by_id(db, goal_id, user_id)
    if goal:
        await db.delete(goal)
        await db.flush()
    return goal
