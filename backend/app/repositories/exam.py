from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.exam import Exam


async def get_by_id(db: AsyncSession, exam_id: UUID, user_id: UUID):
    result = await db.execute(
        select(Exam).where(
            Exam.id == exam_id,
            Exam.user_id == user_id,
        )
    )
    return result.scalar_one_or_none()


async def get_multi(db: AsyncSession, user_id: UUID):
    result = await db.execute(select(Exam).where(Exam.user_id == user_id))
    return list(result.scalars().all())


async def create(db: AsyncSession, *, data: dict):
    exam = Exam(**data)
    db.add(exam)
    await db.flush()
    await db.refresh(exam)
    return exam


async def update(db: AsyncSession, *, exam: Exam, data: dict):
    for field, value in data.items():
        setattr(exam, field, value)
    await db.flush()
    await db.refresh(exam)
    return exam


async def delete(db: AsyncSession, exam_id: UUID, user_id: UUID):
    exam = await get_by_id(db, exam_id, user_id)
    if exam:
        await db.delete(exam)
        await db.flush()
    return exam
