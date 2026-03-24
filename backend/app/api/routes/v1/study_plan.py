from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user, get_db_session
from app.schemas.study_plan import StudyPlanCreate
from app.services.study_plan import StudyPlanService

router = APIRouter()


@router.post("/")
async def create_plan(
    data: StudyPlanCreate,
    db: AsyncSession = Depends(get_db_session),
    user=Depends(get_current_user),
):
    service = StudyPlanService(db)
    return await service.create(user.id, data)


@router.get("/")
async def get_plans(
    db: AsyncSession = Depends(get_db_session),
    user=Depends(get_current_user),
):
    service = StudyPlanService(db)
    return await service.get_all(user.id)
