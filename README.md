# FastAPI Todo

Commands
```bash
uvicorn todo.main:app --host 0.0.0.0 --port 8000 --reload

poetry run task --list


poetry run shell


black .
flake8
pytest
pytest --cov=todo

docker compose exec postgres psql --username=todo --dbname=db_todo
  \l    list databases
  \dt   list tables
  \du   list roles

docker-compose down -v


```


```bash

alembic revision --autogenerate -m "init"
alembic upgrade head

```

TODO
fastapi-users
python-multipart = "^0.0.9"
watchgod = "^0.8.2"
factory-boy = "^3.2.1"
pre-commit = "^3.1.1"
isort = "^5.12.0"


CHECK IT OUT
creating two db in the same db instance
https://www.youtube.com/watch?v=UVBrRKgnJB4
https://github.com/amarjanica/docker-multi-postgres-databases


Links:
- https://testdriven.io/blog/fastapi-sqlmodel/#alembic
- https://fastapi.tiangolo.com/pt/tutorial/handling-errors/
- https://github.com/Riverfount/todo-project/
- https://github.com/Netflix/dispatch/
- https://github.com/MagicStack/asyncpg
- https://testcontainers.com/
- https://medium.com/@johnidouglasmarangon/using-migrations-in-python-sqlalchemy-with-alembic-docker-solution-bd79b219d6a
- https://thinhdanggroup.github.io/alembic-python/


ASYNC
https://github.com/gaganpreet/fastapi-starter/blob/main/%7B%7Bcookiecutter.project_slug%7D%7D/backend/tests/conftest.py
https://github.com/gaganpreet/fastapi-starter/blob/main/%7B%7Bcookiecutter.project_slug%7D%7D/backend/pyproject.toml

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

engine = create_async_engine(
    settings.PDR_DATABASE_URL,
    pool_size=300,
    max_overflow=0,
    pool_timeout=20,
    connect_args={"timeout": 20},
)

async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

@contextlib.asynccontextmanager
async def get_session() -> AsyncSession:
    """[summary]

    :return: It yields the async session established with the database
    :rtype: Iterator[AsyncSession]
    """
    async with async_session() as session:
        try:
            yield session
        except TimeoutError as te:
            await session.close()
            raise te
        except InvalidPasswordError as ipe:
            await session.close()
            raise ipe
        except:
            await session.rollback()
            raise
        finally:
            await session.close()