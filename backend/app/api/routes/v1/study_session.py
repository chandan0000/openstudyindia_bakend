from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user, get_db_session
from app.schemas.study_session import SessionStart
from app.services.study_session import StudySessionService

router = APIRouter()


@router.post("/start")
async def start_session(
    data: SessionStart,
    db: AsyncSession = Depends(get_db_session),
    user=Depends(get_current_user),
):
    service = StudySessionService(db)
    return await service.start(user.id, data.topic_id)


@router.post("/end")
async def end_session(
    db: AsyncSession = Depends(get_db_session),
    user=Depends(get_current_user),
):
    service = StudySessionService(db)
    return await service.end(user.id)


@router.get("/")
async def get_sessions(
    db: AsyncSession = Depends(get_db_session),
    user=Depends(get_current_user),
):
    service = StudySessionService(db)
    return await service.get_all(user.id)
