from uuid import UUID

from fastapi import APIRouter, Depends
from fastapi_pagination import Page
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user, get_db_session
from app.schemas.study_plan import StudyPlanCreate, StudyPlanResponse, StudyPlanUpdate
from app.services.study_plan import StudyPlanService

router = APIRouter()


@router.post("/", response_model=StudyPlanResponse)
async def create_plan(
    data: StudyPlanCreate,
    db: AsyncSession = Depends(get_db_session),
    user=Depends(get_current_user),
):
    service = StudyPlanService(db)
    return await service.create(user.id, data)


@router.get("/", response_model=Page[StudyPlanResponse])
async def get_plans(
    db: AsyncSession = Depends(get_db_session),
    user=Depends(get_current_user),
):
    from fastapi_pagination.ext.sqlalchemy import paginate
    from sqlalchemy import select

    from app.db.models.study_plan import StudyPlan

    query = select(StudyPlan).where(StudyPlan.user_id == user.id)
    return await paginate(db, query)


@router.get("/{plan_id}", response_model=StudyPlanResponse)
async def get_plan(
    plan_id: UUID,
    db: AsyncSession = Depends(get_db_session),
    user=Depends(get_current_user),
):
    service = StudyPlanService(db)
    return await service.get_by_id(plan_id, user.id)


@router.put("/{plan_id}", response_model=StudyPlanResponse)
async def update_plan(
    plan_id: UUID,
    data: StudyPlanUpdate,
    db: AsyncSession = Depends(get_db_session),
    user=Depends(get_current_user),
):
    service = StudyPlanService(db)
    return await service.update(plan_id, user.id, data)


@router.delete("/{plan_id}")
async def delete_plan(
    plan_id: UUID,
    db: AsyncSession = Depends(get_db_session),
    user=Depends(get_current_user),
):
    service = StudyPlanService(db)
    await service.delete(plan_id, user.id)
    return {"message": "Study plan deleted successfully"}
