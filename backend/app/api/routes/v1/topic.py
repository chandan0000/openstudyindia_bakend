from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user, get_db_session
from app.schemas.custom_page import CustomPage
from app.schemas.topic import TopicCreate, TopicResponse, TopicUpdate
from app.services.topic import TopicService

router = APIRouter()


@router.post("/", response_model=TopicResponse)
async def create_topic(
    data: TopicCreate,
    db: AsyncSession = Depends(get_db_session),
    user=Depends(get_current_user),
):
    service = TopicService(db)
    return await service.create(user.id, data)


@router.get("/", response_model=CustomPage[TopicResponse])
async def get_topics(
    subject_id: UUID = Query(...),
    db: AsyncSession = Depends(get_db_session),
    user=Depends(get_current_user),
):
    from fastapi_pagination.ext.sqlalchemy import paginate
    from sqlalchemy import select

    from app.db.models.topic import Topic

    # Check subject ownership first
    from app.repositories import subject_repo

    subject = await subject_repo.get_by_id(db, subject_id, user.id)
    if not subject:
        from app.core.exceptions import NotFoundError

        raise NotFoundError("Subject not found")

    query = select(Topic).where(Topic.subject_id == subject_id)
    return await paginate(db, query)


@router.get("/{topic_id}", response_model=TopicResponse)
async def get_topic(
    topic_id: UUID,
    db: AsyncSession = Depends(get_db_session),
    user=Depends(get_current_user),
):
    service = TopicService(db)
    return await service.get_by_id(topic_id, user.id)


@router.put("/{topic_id}", response_model=TopicResponse)
async def update_topic(
    topic_id: UUID,
    data: TopicUpdate,
    db: AsyncSession = Depends(get_db_session),
    user=Depends(get_current_user),
):
    service = TopicService(db)
    return await service.update(topic_id, user.id, data)


@router.delete("/{topic_id}")
async def delete_topic(
    topic_id: UUID,
    db: AsyncSession = Depends(get_db_session),
    user=Depends(get_current_user),
):
    service = TopicService(db)
    await service.delete(topic_id, user.id)
    return {"message": "Topic deleted successfully"}
