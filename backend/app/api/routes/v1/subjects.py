from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user, get_db_session
from app.schemas.custom_page import CustomPage
from app.schemas.subject import SubjectCreate, SubjectResponse, SubjectUpdate
from app.services.subject import SubjectService

router = APIRouter()


@router.post("/", response_model=SubjectResponse)
async def create_subject(
    data: SubjectCreate,
    db: AsyncSession = Depends(get_db_session),
    user=Depends(get_current_user),
):
    service = SubjectService(db)
    return await service.create(user.id, data)


@router.get("/", response_model=CustomPage[SubjectResponse])
async def get_subjects(
    db: AsyncSession = Depends(get_db_session),
    user=Depends(get_current_user),
):
    from fastapi_pagination.ext.sqlalchemy import paginate
    from sqlalchemy import select

    from app.db.models.subjects import Subjects

    query = select(Subjects).where(Subjects.user_id == user.id)
    return await paginate(db, query)


@router.get("/{subject_id}", response_model=SubjectResponse)
async def get_subject(
    subject_id: UUID,
    db: AsyncSession = Depends(get_db_session),
    user=Depends(get_current_user),
):
    service = SubjectService(db)
    return await service.get_by_id(subject_id, user.id)


@router.put("/{subject_id}", response_model=SubjectResponse)
async def update_subject(
    subject_id: UUID,
    data: SubjectUpdate,
    db: AsyncSession = Depends(get_db_session),
    user=Depends(get_current_user),
):
    service = SubjectService(db)
    return await service.update(subject_id, user.id, data)


@router.delete("/{subject_id}")
async def delete_subject(
    subject_id: UUID,
    db: AsyncSession = Depends(get_db_session),
    user=Depends(get_current_user),
):
    service = SubjectService(db)
    await service.delete(subject_id, user.id)
    return {"message": "Subject deleted successfully"}
