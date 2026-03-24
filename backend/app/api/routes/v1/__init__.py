"""API v1 router aggregation."""
# ruff: noqa: I001 - Imports structured for Jinja2 template conditionals

from fastapi import APIRouter

from app.api.routes.v1 import health
from app.api.routes.v1 import auth, users
from app.api.routes.v1 import subjects
from app.api.routes.v1 import study_plan
from app.api.routes.v1 import topic
from app.api.routes.v1 import study_session
from app.api.routes.v1 import goals
from app.api.routes.v1 import exam

v1_router = APIRouter()

# Health check routes (no auth required)
v1_router.include_router(health.router, tags=["health"])

# Authentication routes
v1_router.include_router(auth.router, prefix="/auth", tags=["auth"])

# User routes
v1_router.include_router(users.router, prefix="/users", tags=["users"])

v1_router.include_router(subjects.router, prefix="/subjects", tags=["subjects"])
v1_router.include_router(study_plan.router, prefix="/study-plans", tags=["study_plans"])
v1_router.include_router(topic.router, prefix="/topics", tags=["topics"])
v1_router.include_router(study_session.router, prefix="/sessions", tags=["sessions"])
v1_router.include_router(goals.router, prefix="/goals", tags=["goals"])
v1_router.include_router(exam.router, prefix="/exams", tags=["exams"])
