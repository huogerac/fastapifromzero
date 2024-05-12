from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from todo.routers import main_router
from todo.settings import Settings
from todo.exceptions import BusinessError


settings = Settings()
app = FastAPI(title="Todo List", version="0.1.0", description="Fastapi from zero")

app.include_router(main_router)


@app.get("/")
async def home():
    return {
        "db_url": settings.DATABASE_URL,
    }


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    def parse_input_validation(error):
        field = ".".join(error.get("loc"))
        return f"{field}: {error.get('msg')} ({error.get('type')})"

    error = ""
    if len(exc.errors()) >= 1:
        error = parse_input_validation(exc.errors()[0])
    return JSONResponse(
        status_code=422,
        content={
            "message": f"[INVALID INPUT] {error}",
        },
    )


@app.exception_handler(BusinessError)
async def business_exception_handler(request: Request, exc: BusinessError):
    error = str(exc)
    return JSONResponse(
        status_code=400,
        content={
            "message": f"[ERROR] {error}",
        },
    )
