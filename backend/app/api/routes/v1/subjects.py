from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user, get_db_session
from app.schemas.subject import SubjectCreate
from app.services.subject import SubjectService

router = APIRouter()


@router.post("/")
async def create_subject(
    data: SubjectCreate,
    db: AsyncSession = Depends(get_db_session),
    user=Depends(get_current_user),
):
    service = SubjectService(db)
    return await service.create(user.id, data)


@router.get("/")
async def get_subjects(
    db: AsyncSession = Depends(get_db_session),
    user=Depends(get_current_user),
):
    service = SubjectService(db)
    return await service.get_all(user.id)
