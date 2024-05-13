from sqlalchemy import select
from todo.settings import Settings


def test_create_tournament(session):

    result = session.scalar(select(40 + 2))

    assert result == 42


def test_deve_garantir_que_pytest_usa_db_de_teste():

    assert Settings().DATABASE_URL.endswith("_test")
