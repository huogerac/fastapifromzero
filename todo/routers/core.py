from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio.session import AsyncSession
from typing import List

from todo.schemas.core import TaskSchema
from todo.database import get_session

router = APIRouter()


@router.get("/status", response_model=dict)
async def get_status():
    """Get status"""
    response = {
        "status": "ok",
    }
    return response


@router.get("/tasks", response_model=List[TaskSchema])
async def get_tasks(session: AsyncSession = Depends(get_session)):
    """Get tasks"""
    response = []
    return response
