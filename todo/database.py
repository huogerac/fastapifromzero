from sqlalchemy import create_engine
from sqlalchemy.orm import Session, registry

from todo.settings import Settings

engine = create_engine(Settings().DATABASE_URL)
table_registry = registry()


def get_session():
    with Session(engine) as session:
        yield session
