import pytest
from fastapi.testclient import TestClient

from sqlalchemy.orm import Session

from todo.main import app
from todo.database import engine
from todo.models.core import table_registry


@pytest.fixture()
def client():
    return TestClient(app)


@pytest.fixture()
def session():
    table_registry.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
    table_registry.metadata.drop_all(engine)


# from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
# from sqlalchemy import select
# async_sessionmaker[AsyncSession]
