from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.subjects import Subjects


async def get_by_id(db: AsyncSession, Subjects_id: UUID) -> Subjects | None:
    return await db.get(Subjects, Subjects_id)


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


async def delete(db: AsyncSession, Subjects_id: UUID) -> Subjects | None:
    subject = await get_by_id(db, Subjects_id)
    if subject:
        await db.delete(subject)
        await db.flush()
    return subject
