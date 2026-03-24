from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.topic import Topic


async def get_by_id(db: AsyncSession, topic_id: UUID) -> Topic | None:
    return await db.get(Topic, topic_id)


async def get_by_name(
    db: AsyncSession,
    subject_id: UUID,
    name: str,
) -> Topic | None:
    result = await db.execute(
        select(Topic).where(
            Topic.subject_id == subject_id,
            Topic.name == name,
        )
    )
    return result.scalar_one_or_none()


async def get_multi(
    db: AsyncSession,
    subject_id: UUID,
) -> list[Topic]:
    result = await db.execute(select(Topic).where(Topic.subject_id == subject_id))
    return list(result.scalars().all())


async def create(
    db: AsyncSession,
    *,
    subject_id: UUID,
    name: str,
) -> Topic:
    topic = Topic(subject_id=subject_id, name=name)
    db.add(topic)
    await db.flush()
    await db.refresh(topic)
    return topic


async def delete(db: AsyncSession, topic_id: UUID) -> Topic | None:
    topic = await get_by_id(db, topic_id)
    if topic:
        await db.delete(topic)
        await db.flush()
    return topic
