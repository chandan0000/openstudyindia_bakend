from datetime import UTC, datetime
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user, get_db_session
from app.schemas.custom_page import CustomPage
from app.schemas.exam import ExamCreate, ExamResponse, ExamUpdate
from app.services.exam import ExamService

router = APIRouter()


@router.post("/", response_model=ExamResponse)
async def create_exam(
    data: ExamCreate,
    db: AsyncSession = Depends(get_db_session),
    user=Depends(get_current_user),
):
    service = ExamService(db)
    exam = await service.create(user.id, data)
    # Add days_left
    now = datetime.now(UTC)
    days_left = max(0, (exam.exam_date - now).days)
    exam.days_left = days_left
    return exam


@router.get("/", response_model=CustomPage[ExamResponse])
async def get_exams(
    db: AsyncSession = Depends(get_db_session),
    user=Depends(get_current_user),
):
    from fastapi_pagination.ext.sqlalchemy import paginate
    from sqlalchemy import select

    from app.db.models.exam import Exam

    query = select(Exam).where(Exam.user_id == user.id)
    page = await paginate(db, query)

    # Add days_left to each item
    now = datetime.now(UTC)
    for exam in page.items:
        days_left = max(0, (exam.exam_date - now).days)
        exam.days_left = days_left

    return page


@router.get("/{exam_id}", response_model=ExamResponse)
async def get_exam(
    exam_id: UUID,
    db: AsyncSession = Depends(get_db_session),
    user=Depends(get_current_user),
):
    service = ExamService(db)
    exam = await service.get_by_id(exam_id, user.id)
    # Add days_left
    now = datetime.now(UTC)
    days_left = max(0, (exam.exam_date - now).days)
    exam.days_left = days_left
    return exam


@router.put("/{exam_id}", response_model=ExamResponse)
async def update_exam(
    exam_id: UUID,
    data: ExamUpdate,
    db: AsyncSession = Depends(get_db_session),
    user=Depends(get_current_user),
):
    service = ExamService(db)
    exam = await service.update(exam_id, user.id, data)
    # Add days_left
    now = datetime.now(UTC)
    days_left = max(0, (exam.exam_date - now).days)
    exam.days_left = days_left
    return exam


@router.delete("/{exam_id}")
async def delete_exam(
    exam_id: UUID,
    db: AsyncSession = Depends(get_db_session),
    user=Depends(get_current_user),
):
    service = ExamService(db)
    await service.delete(exam_id, user.id)
    return {"message": "Exam deleted successfully"}
