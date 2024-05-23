from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio.session import AsyncSession

from todo.database import get_session
from todo.schemas.core import TaskSchema, TaskSchemaIn, ListTasksSchema
from todo.schemas.base import Error
from todo.services import tasks_service
from todo.services.auth_service import login_required

router = APIRouter()


@router.get(
    "/tasks/list",
    response_model=ListTasksSchema,
    responses={401: {"model": Error}, 422: {"model": Error, "description": "Bad Request"}},
)
@login_required()
async def get_tasks(request: Request, session: AsyncSession = Depends(get_session)):
    """Lista tasks"""
    response = {"tasks": tasks_service.list_tasks(session)}
    return response


@router.post(
    "/tasks/add",
    response_model=TaskSchema,
    status_code=201,
    responses={401: {"model": Error}, 422: {"model": Error, "description": "Bad Request"}},
)
@login_required()
async def add_tasks(request: Request, task: TaskSchemaIn, session: AsyncSession = Depends(get_session)):
    """Adiciona Task"""
    response = tasks_service.add_task(session, task.description)
    return response
