from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import NotFoundError
from app.repositories import goal as repo


class GoalService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, user_id: UUID, data):
        return await repo.create(
            self.db,
            data={
                "user_id": user_id,
                "title": data.title,
                "target_value": data.target_value,
                "deadline": data.deadline,
            },
        )

    async def get_all(self, user_id: UUID):
        return await repo.get_multi(self.db, user_id)

    async def update(self, goal_id: UUID, data):
        goal = await repo.get_by_id(self.db, goal_id)
        if not goal:
            raise NotFoundError(message="Goal not found")

        return await repo.update(
            self.db,
            goal,
            data=data.model_dump(exclude_unset=True, exclude_none=True),
        )

    async def delete(self, goal_id: UUID):
        goal = await repo.delete(self.db, goal_id)
        if not goal:
            raise NotFoundError(message="Goal not found")
        return goal
