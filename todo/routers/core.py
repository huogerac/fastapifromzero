from fastapi import APIRouter

router = APIRouter()


@router.get("/status", response_model=dict)
async def get_status():
    """Get status"""
    response = {"status": "ok"}
    return response
