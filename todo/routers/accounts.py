from fastapi import APIRouter, Depends, Request, Response
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio.session import AsyncSession

from todo.database import get_session
from todo.schemas.accounts import UserSchema, LoginSchema, LoggedUserSchema
from todo.schemas.base import Error
from todo.services import auth_service

router = APIRouter()
_14DAYS = 1209600


# username: Annotated[str, Form()], password: Annotated[str, Form()]
@router.post(
    "/login",
    response_model=UserSchema,
    status_code=201,
    responses={401: {"model": Error}, 422: {"model": Error, "description": "Bad Request"}},
)
async def login(data: LoginSchema, session: AsyncSession = Depends(get_session)):
    """
    Login do usuário e criação de uma nova sessão\n
    **Parameters**:\n
        - email* (str): email para login
        - password* (str): senha
    **Returns**:\n
        - dados do usuário logado
    """
    user_session = auth_service.login(session, data.email, data.password)
    response = JSONResponse(content=user_session["user"], status_code=201)
    response.set_cookie(key="sessionid", value=user_session.get("session_id"), httponly=True, max_age=_14DAYS)
    return response


@router.post("/logout", response_model=dict)
async def logout(request: Request, response: Response, session: AsyncSession = Depends(get_session)):
    """
    Encerra sessão do usuário
    """
    if request.state.user and request.state.sessionid:
        session_id = auth_service.logout(session, request.state.sessionid)
        if session_id:
            response.delete_cookie(session_id)
    response = {}
    return response


@router.get("/whoami", response_model=LoggedUserSchema, status_code=200, response_model_exclude_none=True)
async def whoami(request: Request, session: AsyncSession = Depends(get_session)):
    content = {"authenticated": False}
    if request.state.user:
        content["authenticated"] = True
        content["user"] = request.state.user.to_dict_json()
    # logger.info("API whoami")
    return content
