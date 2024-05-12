from sqlalchemy import select


def test_create_tournament(session):

    result = session.scalar(select(40 + 2))

    assert result == 42
