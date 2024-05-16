import pytest
from fastapi.testclient import TestClient
from fastapi import Request
from sqlalchemy.orm import Session

from todo.main import app
from todo.database import engine
from todo.models.core import table_registry
from todo.main import SessionIdMiddleware as OriginSessionIdMiddleware


class SessionMiddleware(OriginSessionIdMiddleware):

    async def dispatch(self, request: Request, call_next):

        request.state.sessionid = "sessionid-test"
        request.state.user = None
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


# from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
# from sqlalchemy import select
# async_sessionmaker[AsyncSession]
