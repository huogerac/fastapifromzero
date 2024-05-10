from fastapi import FastAPI

from todo.routers import main_router
from todo.settings import Settings


settings = Settings()
app = FastAPI(title="Todo List", version="0.1.0", description="Fastapi from zero")

app.include_router(main_router)


@app.get("/")
async def home():
    return {
        "db_url": settings.DATABASE_URL,
    }
