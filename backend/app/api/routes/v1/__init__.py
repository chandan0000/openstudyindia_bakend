from fastapi import APIRouter

from app.api.routes.v1 import (
    auth,
    exam,
    goals,
    health,
    study_plan,
    study_session,
    subjects,
    topic,
    users,
)

v1_router = APIRouter()

v1_router.include_router(health.router, tags=["health"])

v1_router.include_router(auth.router, prefix="/auth", tags=["auth"])

v1_router.include_router(users.router, prefix="/users", tags=["users"])

v1_router.include_router(subjects.router, prefix="/subjects", tags=["subjects"])
v1_router.include_router(topic.router, prefix="/topics", tags=["topics"])

v1_router.include_router(study_plan.router, prefix="/study-plans", tags=["study_plans"])

v1_router.include_router(study_session.router, prefix="/sessions", tags=["sessions"])

v1_router.include_router(goals.router, prefix="/goals", tags=["goals"])
v1_router.include_router(exam.router, prefix="/exams", tags=["exams"])
