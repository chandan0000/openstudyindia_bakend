from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.subjects import Subjects


async def get_by_id(db: AsyncSession, subject_id: UUID, user_id: UUID) -> Subjects | None:
    result = await db.execute(
        select(Subjects).where(
            Subjects.id == subject_id,
            Subjects.user_id == user_id,
        )
    )
    return result.scalar_one_or_none()


async def get_by_name(db: AsyncSession, user_id: UUID, name: str) -> Subjects | None:
    result = await db.execute(
        select(Subjects).where(
            Subjects.user_id == user_id,
            Subjects.name == name,
        )
    )
    return result.scalar_one_or_none()


async def get_multi(db: AsyncSession, user_id: UUID) -> list[Subjects]:
    result = await db.execute(select(Subjects).where(Subjects.user_id == user_id))
    return list(result.scalars().all())


async def create(db: AsyncSession, *, user_id: UUID, name: str) -> Subjects:
    subject = Subjects(user_id=user_id, name=name)
    db.add(subject)
    await db.flush()
    await db.refresh(subject)
    return subject


async def update(db: AsyncSession, *, subject: Subjects, data: dict) -> Subjects:
    for key, value in data.items():
        setattr(subject, key, value)
    await db.flush()
    await db.refresh(subject)
    return subject


async def delete(db: AsyncSession, subject_id: UUID, user_id: UUID) -> Subjects | None:
    subject = await get_by_id(db, subject_id, user_id)
    if subject:
        await db.delete(subject)
        await db.flush()
    return subject
