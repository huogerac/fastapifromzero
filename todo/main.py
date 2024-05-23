from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware

from todo.routers import main_router
from todo.settings import Settings
from todo.exceptions import BusinessError, UnauthorizedException, ConflictValueException
from todo.services.auth_service import SessionIdMiddleware

settings = Settings()

app = FastAPI(
    title="Todo List",
    version="0.1.0",
    description="Fastapi from zero",
    docs_url="/api/docs",
)

origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:3000",
]

app.include_router(main_router)
app.add_middleware(SessionIdMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "message": f"[ERROR] {error}",
        },
    )


@app.exception_handler(UnauthorizedException)
async def unauthorized_exception_handler(request: Request, exc: UnauthorizedException):
    error = str(exc)
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={
            "message": f"[ACCESS ERROR] {error}",
        },
    )


@app.exception_handler(ConflictValueException)
async def conflict_exception_handler(request: Request, exc: ConflictValueException):
    error = str(exc)
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={
            "message": f"[DATA ERROR] {error}",
        },
    )


@app.exception_handler(Exception)
async def internal_exception_handler(request: Request, exc: Exception):
    error = str(exc)
    return JSONResponse(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        content={"message": f"""[UNAVAILABLE] Opps! Serviço não disponível no momento. Tente mais tarde: {error}"""},
    )


# @app.middleware("http")
# async def sessionid_middleware_header(request: Request, call_next):
#     db_session = next(get_session())
#     sessionid = request.cookies.get("sessionid")
#     request.state.sessionid = sessionid
#     request.state.user = get_user_by_sessionid(db_session, sessionid)
#     response = await call_next(request)
#     return response
