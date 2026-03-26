from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user, get_db_session
from app.schemas.custom_page import CustomPage
from app.schemas.goal import GoalCreate, GoalResponse, GoalUpdate
from app.services.goal import GoalService

router = APIRouter()


@router.post("/", response_model=GoalResponse)
async def create_goal(
    data: GoalCreate,
    db: AsyncSession = Depends(get_db_session),
    user=Depends(get_current_user),
):
    service = GoalService(db)
    return await service.create(user.id, data)


@router.get("/", response_model=CustomPage[GoalResponse])
async def get_goals(
    db: AsyncSession = Depends(get_db_session),
    user=Depends(get_current_user),
):
    from fastapi_pagination.ext.sqlalchemy import paginate
    from sqlalchemy import select

    from app.db.models.goal import Goal

    query = select(Goal).where(Goal.user_id == user.id)
    return await paginate(db, query)


@router.get("/{goal_id}", response_model=GoalResponse)
async def get_goal(
    goal_id: UUID,
    db: AsyncSession = Depends(get_db_session),
    user=Depends(get_current_user),
):
    service = GoalService(db)
    return await service.get_by_id(goal_id, user.id)


@router.put("/{goal_id}", response_model=GoalResponse)
async def update_goal(
    goal_id: UUID,
    data: GoalUpdate,
    db: AsyncSession = Depends(get_db_session),
    user=Depends(get_current_user),
):
    service = GoalService(db)
    return await service.update(goal_id, user.id, data)


@router.delete("/{goal_id}")
async def delete_goal(
    goal_id: UUID,
    db: AsyncSession = Depends(get_db_session),
    user=Depends(get_current_user),
):
    service = GoalService(db)
    await service.delete(goal_id, user.id)
    return {"message": "Goal deleted successfully"}
