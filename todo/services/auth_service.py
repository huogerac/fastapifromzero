import os
import random
import uuid
from passlib.context import CryptContext

from todo.models.users import User, UserSession
from todo.exceptions import UnauthorizedException

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


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


def get_password_hash(plain_password):
    return pwd_context.hash(plain_password)


def check_password_hash(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def add_new_session(session, user_id: int) -> dict:
    new_session = UserSession(user_id=user_id, session_id=generate_sessionid())
    session.add(new_session)
    session.commit()
    session.refresh(new_session)
    return new_session.to_dict_json()


def get_user_by_sessionid(session, session_id: int):
    user_session = session.query(UserSession).filter(UserSession.session_id == session_id).first()
    if not user_session:
        return None
    user = session.query(User).filter(User.id == user_session.user_id).first()
    return user


def generate_sessionid():
    return uuid.uuid5(uuid.NAMESPACE_DNS, f"{uuid.uuid1()}{random.random()}{os.getpid()}").hex
