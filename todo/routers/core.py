from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio.session import AsyncSession

from todo.database import get_session
from todo.schemas.core import TaskSchema, TaskSchemaIn, ListTasksSchema
from todo.services import tasks_service

router = APIRouter()


@router.get("/status", response_model=dict)
async def get_status():
    """Get status"""
    response = {
        "status": "ok",
    }
    return response


@router.get("/tasks", response_model=ListTasksSchema)
async def get_tasks(session: AsyncSession = Depends(get_session)):
    """Get tasks"""
    response = {"tasks": tasks_service.list_tasks(session)}
    return response


@router.post("/tasks", response_model=TaskSchema, status_code=201)
async def add_tasks(session: AsyncSession = Depends(get_session), task: TaskSchemaIn = None):
    """Create a new task"""
    response = tasks_service.add_task(session, task.description)
    return response
