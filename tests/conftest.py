import pytest
from fastapi.testclient import TestClient

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from todo.main import app
from todo.models.core import table_registry


@pytest.fixture()
def client():
    return TestClient(app)


@pytest.fixture()
def session():
    engine = create_engine('sqlite:///:memory:')
    table_registry.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    table_registry.metadata.drop_all(engine)

# @pytest.fixture
# def session():
#     engine = create_engine(
#         'sqlite:///:memory:',
#         connect_args={'check_same_thread': False},
#         poolclass=StaticPool,
#     )
#     Base.metadata.create_all(engine)

#     Session = sessionmaker(bind=engine)

#     yield Session()

#     Base.metadata.drop_all(engine)


#from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
#from sqlalchemy import select
# async_sessionmaker[AsyncSession]