# from functools import wraps
# from fastapi import APIRouter, Depends, Request
# from sqlalchemy.ext.asyncio.session import AsyncSession

# from todo.database import get_session
# from todo.schemas.users import UserSchema, UserSchemaIn, ListUsersSchema
# from todo.services import users_service, auth_service
# from todo.exceptions import UnauthorizedException

# router = APIRouter()


# def login_required():
#     def outer_wrapper(function):
#         @wraps(function)
#         async def inner_wrapper(*args, **kwargs):
#             request = kwargs.get("request")
#             if not request.state.user:
#                 raise UnauthorizedException("Not authorized")
#             return await function(*args, **kwargs)

#         return inner_wrapper

#     return outer_wrapper


# @router.get("/users", response_model=ListUsersSchema)
# @login_required()
# async def get_users(request: Request, session: AsyncSession = Depends(get_session)):
#     """Get tasks"""
#     response = {"users": users_service.list_users(session)}
#     return response


# @router.post("/users", response_model=UserSchema, status_code=201)
# async def add_new_user(session: AsyncSession = Depends(get_session), task: UserSchemaIn = None):
#     """Create a new user"""
#     response = users_service.add_task(session, task.description)
#     return response


# def get_user_from_sessionid(session: AsyncSession = Depends(get_session), session_id: int = None):
#     return auth_service.get_user_by_sessionid(session, session_id)
