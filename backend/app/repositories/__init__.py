"""Repository layer for database operations."""
# ruff: noqa: I001, RUF022 - Imports structured for Jinja2 template conditionals

from app.repositories.base import BaseRepository

from app.repositories import user as user_repo
from app.repositories import subject as subject_repo
from app.repositories import study_plan as study_plan_repo
from app.repositories import topic as topic_repo
from app.repositories import study_session as study_session_repo
from app.repositories import goal as goal_repo
from app.repositories import exam as exam_repo


__all__ = [
    "BaseRepository",
    "user_repo",
    "subject_repo",
    "study_plan_repo",
    "topic_repo",
    "study_session_repo",
    "goal_repo",
    "exam_repo",
]
