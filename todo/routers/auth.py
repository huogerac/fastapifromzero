from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio.session import AsyncSession

from todo.database import get_session
from todo.schemas.users import UserSchema, UserLoginSchema
from todo.services import auth_service

router = APIRouter()


@router.post("/login", response_model=UserSchema)
async def login(session: AsyncSession = Depends(get_session), user: UserLoginSchema = None):
    """Login"""
    user_session = auth_service.login(session, user.email, user.password)
    response = JSONResponse(content={"msg": "user logged in"})
    response.set_cookie(key="sessionid", value=user_session.get("session_id"), httponly=True, max_age=1209600)
    return response
