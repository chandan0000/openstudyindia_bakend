from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user, get_db_session
from app.schemas.goal import GoalCreate, GoalUpdate
from app.services.goal import GoalService

router = APIRouter()


@router.post("/")
async def create_goal(
    data: GoalCreate,
    db: AsyncSession = Depends(get_db_session),
    user=Depends(get_current_user),
):
    return await GoalService(db).create(user.id, data)


@router.get("/")
async def get_goals(
    db: AsyncSession = Depends(get_db_session),
    user=Depends(get_current_user),
):
    return await GoalService(db).get_all(user.id)


@router.patch("/{goal_id}")
async def update_goal(
    goal_id: UUID,
    data: GoalUpdate,
    db: AsyncSession = Depends(get_db_session),
):
    return await GoalService(db).update(goal_id, data)


@router.delete("/{goal_id}")
async def delete_goal(
    goal_id: UUID,
    db: AsyncSession = Depends(get_db_session),
):
    return await GoalService(db).delete(goal_id)
