from fastapi import APIRouter

from .core import router as router_core

main_router = APIRouter()

main_router.include_router(router_core, prefix="/api/core", tags=["core"])
