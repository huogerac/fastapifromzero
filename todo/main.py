from fastapi import FastAPI
from todo.routers import main_router

app = FastAPI(title="Todo List", version="0.1.0", description="Fastapi from zero")

app.include_router(main_router)
