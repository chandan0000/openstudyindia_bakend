from uuid import UUID

from fastapi import APIRouter, Depends
from fastapi_pagination import Page
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user, get_db_session
from app.schemas.study_session import SessionResponse, SessionStart, SessionUpdate
from app.services.study_session import StudySessionService

router = APIRouter()


@router.post("/start", response_model=SessionResponse)
async def start_session(
    data: SessionStart,
    db: AsyncSession = Depends(get_db_session),
    user=Depends(get_current_user),
):
    service = StudySessionService(db)
    return await service.start(user.id, data)


@router.post("/end", response_model=SessionResponse)
async def end_session(
    db: AsyncSession = Depends(get_db_session),
    user=Depends(get_current_user),
):
    service = StudySessionService(db)
    return await service.end(user.id)


@router.get("/", response_model=Page[SessionResponse])
async def get_sessions(
    db: AsyncSession = Depends(get_db_session),
    user=Depends(get_current_user),
):
    from fastapi_pagination.ext.sqlalchemy import paginate
    from sqlalchemy import select

    from app.db.models.study_session import StudySession

    query = select(StudySession).where(StudySession.user_id == user.id)
    return await paginate(db, query)


@router.get("/{session_id}", response_model=SessionResponse)
async def get_session(
    session_id: UUID,
    db: AsyncSession = Depends(get_db_session),
    user=Depends(get_current_user),
):
    service = StudySessionService(db)
    return await service.get_by_id(session_id, user.id)


@router.put("/{session_id}", response_model=SessionResponse)
async def update_session(
    session_id: UUID,
    data: SessionUpdate,
    db: AsyncSession = Depends(get_db_session),
    user=Depends(get_current_user),
):
    service = StudySessionService(db)
    return await service.update(session_id, user.id, data)


@router.delete("/{session_id}")
async def delete_session(
    session_id: UUID,
    db: AsyncSession = Depends(get_db_session),
    user=Depends(get_current_user),
):
    service = StudySessionService(db)
    await service.delete(session_id, user.id)
    return {"message": "Study session deleted successfully"}
