from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.study_session import StudySession


async def get_by_id(db: AsyncSession, session_id: UUID, user_id: UUID) -> StudySession | None:
    result = await db.execute(
        select(StudySession).where(
            StudySession.id == session_id,
            StudySession.user_id == user_id,
        )
    )
    return result.scalar_one_or_none()


async def get_active_session(
    db: AsyncSession,
    user_id: UUID,
) -> StudySession | None:
    result = await db.execute(
        select(StudySession).where(
            StudySession.user_id == user_id,
            StudySession.end_time.is_(None),
        )
    )
    return result.scalar_one_or_none()


async def create(
    db: AsyncSession,
    *,
    user_id: UUID,
    topic_id: UUID,
    start_time,
) -> StudySession:
    session = StudySession(
        user_id=user_id,
        topic_id=topic_id,
        start_time=start_time,
    )
    db.add(session)
    await db.flush()
    await db.refresh(session)
    return session


async def update(
    db: AsyncSession,
    session: StudySession,
    data: dict,
) -> StudySession:
    for field, value in data.items():
        setattr(session, field, value)

    db.add(session)
    await db.flush()
    await db.refresh(session)
    return session


async def get_multi(db: AsyncSession, user_id: UUID):
    result = await db.execute(select(StudySession).where(StudySession.user_id == user_id))
    return list(result.scalars().all())


async def delete(db: AsyncSession, session_id: UUID, user_id: UUID) -> StudySession | None:
    session = await get_by_id(db, session_id, user_id)
    if session:
        await db.delete(session)
        await db.flush()
    return session
