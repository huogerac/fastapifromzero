from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio.session import AsyncSession

from todo.database import get_session
from todo.schemas.users import UserSchema, UserSchemaIn, ListUsersSchema
from todo.services import users_service

router = APIRouter()


@router.get("/tasks", response_model=ListUsersSchema)
async def get_tasks(session: AsyncSession = Depends(get_session)):
    """Get tasks"""
    response = {"tasks": users_service.list_tasks(session)}
    return response


@router.post("/users", response_model=UserSchema, status_code=201)
async def add_new_user(session: AsyncSession = Depends(get_session), task: UserSchemaIn = None):
    """Create a new user"""
    response = users_service.add_task(session, task.description)
    return response
