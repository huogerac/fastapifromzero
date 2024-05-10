# FastAPI Todo

Commands
```bash
uvicorn todo.main:app --host 0.0.0.0 --port 8000 --reload

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

Links:
- https://testdriven.io/blog/fastapi-sqlmodel/#alembic
