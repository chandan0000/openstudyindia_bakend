from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.exam import Exam


async def get_by_id(db: AsyncSession, exam_id: UUID):
    return await db.get(Exam, exam_id)


async def get_multi(db: AsyncSession, user_id: UUID):
    result = await db.execute(select(Exam).where(Exam.user_id == user_id))
    return list(result.scalars().all())


async def create(db: AsyncSession, *, data: dict):
    exam = Exam(**data)
    db.add(exam)
    await db.flush()
    await db.refresh(exam)
    return exam


async def delete(db: AsyncSession, exam_id: UUID):
    exam = await get_by_id(db, exam_id)
    if exam:
        await db.delete(exam)
        await db.flush()
    return exam
