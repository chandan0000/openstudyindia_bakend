from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user, get_db_session
from app.schemas.topic import TopicCreate
from app.services.topic import TopicService

router = APIRouter()


@router.post("/")
async def create_topic(
    data: TopicCreate,
    db: AsyncSession = Depends(get_db_session),
    user=Depends(get_current_user),
):
    service = TopicService(db)
    return await service.create(user.id, data)


@router.get("/")
async def get_topics(
    subject_id: UUID = Query(...),
    db: AsyncSession = Depends(get_db_session),
    user=Depends(get_current_user),
):
    service = TopicService(db)
    return await service.get_all(user.id, subject_id)


@router.delete("/{topic_id}")
async def delete_topic(
    topic_id: UUID,
    db: AsyncSession = Depends(get_db_session),
    user=Depends(get_current_user),
):
    service = TopicService(db)
    return await service.delete(user.id, topic_id)
