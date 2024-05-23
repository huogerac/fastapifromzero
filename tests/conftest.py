import pytest
from fastapi.testclient import TestClient
from fastapi import Request
from sqlalchemy.orm import Session
from unittest.mock import MagicMock

from todo.main import app
from todo.database import engine
from todo.models.core import table_registry
from todo.models.users import User
from todo.main import SessionIdMiddleware as OriginSessionIdMiddleware
from todo.services import auth_service


userMock = MagicMock()
userMock.to_dict_json.return_value = {
    "id": 1,
    "username": "jon@doe.com.br",
    "email": "jon@doe.com.br",
    "name": "Jon Doe",
    "created_at": "20240511",
}


def get_session_and_user_for_tests(user_logged_in=False):
    if user_logged_in:
        return "sessionid-mock", userMock
    return (None, None)


class SessionMiddleware(OriginSessionIdMiddleware):

    async def dispatch(self, request: Request, call_next):
        sessionid, user = get_session_and_user_for_tests()
        request.state.sessionid = sessionid
        request.state.user = user
        response = await call_next(request)
        return response


app.user_middleware.clear()
app.add_middleware(SessionMiddleware)
app.middleware_stack = app.build_middleware_stack()


@pytest.fixture(scope="module")
def client():
    client_app = TestClient(app)
    yield client_app


@pytest.fixture()
def session():
    table_registry.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
    table_registry.metadata.drop_all(engine)


@pytest.fixture()
def jon_doe(session):
    new_user = User(
        id=None,
        username="jon@doe.com.br",
        email="jon@doe.com.br",
        name="Jon Doe",
        password=auth_service.get_password_hash("abacate"),
    )

    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user


@pytest.fixture()
def jon_doe_logged():
    return userMock

# from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
# from sqlalchemy import select
# async_sessionmaker[AsyncSession]