import os
import random
import uuid
from functools import wraps
from passlib.context import CryptContext
from passlib.exc import UnknownHashError
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

from todo.exceptions import UnauthorizedException
from todo.database import get_session
from todo.models.users import User, UserSession

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class SessionIdMiddleware(BaseHTTPMiddleware):

    def __init__(self, app):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next):
        db_session = next(get_session())
        check_existing_sessionid(request, db_session)
        response = await call_next(request)
        return response


def check_existing_sessionid(request, db_session):
    sessionid = request.cookies.get("sessionid")
    if sessionid:
        request.state.sessionid = sessionid
        request.state.user = get_user_by_sessionid(db_session, sessionid)


def login_required():
    def outer_wrapper(function):
        @wraps(function)
        async def inner_wrapper(*args, **kwargs):
            request = kwargs.get("request")
            if not request.state.user:
                raise UnauthorizedException("Not authorized")
            return await function(*args, **kwargs)

        return inner_wrapper

    return outer_wrapper


def login(session, email: str, password: str) -> dict:
    user = session.query(User).filter(User.email == email).first()
    if not user:
        raise UnauthorizedException("Credentials or eMail is invalid!")

    valid_password = check_password_hash(password, user.password)
    if not valid_password:
        raise UnauthorizedException("Credentials or eMail is invalid!")

    user_session = add_new_session(session, user.id)
    user_session["user"] = user.to_dict_json()
    return user_session


def logout(session, session_id: str) -> dict:
    user_session = session.query(UserSession).filter(UserSession.session_id == session_id).first()
    if user_session:
        session.delete(user_session)
        session.commit()
        return session_id

    return None


def get_password_hash(plain_password):
    return pwd_context.hash(plain_password)


def check_password_hash(plain_password, hashed_password):
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except UnknownHashError:
        return False


def add_new_session(session, user_id: int) -> dict:
    new_session = UserSession(user_id=user_id, session_id=generate_sessionid())
    session.add(new_session)
    session.commit()
    session.refresh(new_session)
    return new_session.to_dict_json()


def get_user_by_sessionid(session, session_id: str):
    user_session = session.query(UserSession).filter(UserSession.session_id == session_id).first()
    if not user_session:
        return None
    user = session.query(User).filter(User.id == user_session.user_id).first()
    return user


def generate_sessionid():
    return uuid.uuid5(uuid.NAMESPACE_DNS, f"{uuid.uuid1()}{random.random()}{os.getpid()}").hex
