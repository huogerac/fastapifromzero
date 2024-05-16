from fastapi import APIRouter

from .core import router as router_core
from .users import router as router_users
from .auth import router as router_auth

main_router = APIRouter()

main_router.include_router(router_core, prefix="/api/core", tags=["core"])
main_router.include_router(router_users, prefix="/api/users", tags=["users"])
main_router.include_router(router_auth, prefix="/api/auth", tags=["auth"])
