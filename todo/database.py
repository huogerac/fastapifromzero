from sqlalchemy import create_engine

# from sqlalchemy.orm import DeclarativeBase, Session
from sqlalchemy.orm import Session

# from sqlalchemy.orm import declarative_base
# from sqlalchemy.pool import NullPool

from todo.settings import Settings


# engine = create_engine(
#     url=Settings().DATABASE_URL, echo=True, future=True, poolclass=NullPool
# )

engine = create_engine(Settings().DATABASE_URL)

# class Base(DeclarativeBase):
#     pass

# Base = declarative_base()
# base = declarative_base(bind=engine)


def get_session():
    with Session(engine) as session:
        yield session
