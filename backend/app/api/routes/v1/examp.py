from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user, get_db_session
from app.schemas.exam import ExamCreate
from app.services.exam import ExamService

router = APIRouter()


@router.post("/")
async def create_exam(
    data: ExamCreate,
    db: AsyncSession = Depends(get_db_session),
    user=Depends(get_current_user),
):
    return await ExamService(db).create(user.id, data)


@router.get("/")
async def get_exams(
    db: AsyncSession = Depends(get_db_session),
    user=Depends(get_current_user),
):
    return await ExamService(db).get_all(user.id)


@router.delete("/{exam_id}")
async def delete_exam(
    exam_id: UUID,
    db: AsyncSession = Depends(get_db_session),
):
    return await ExamService(db).delete(exam_id)
