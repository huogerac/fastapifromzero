from fastapi import APIRouter

from .base import router as router_base
from .accounts import router as router_auth
from .core import router as router_core

main_router = APIRouter()

main_router.include_router(router_base, prefix="/api", tags=["base"])
main_router.include_router(router_auth, prefix="/api/accounts", tags=["accounts"])
main_router.include_router(router_core, prefix="/api/core", tags=["core"])
# main_router.include_router(router_users, prefix="/api/users", tags=["users"])
