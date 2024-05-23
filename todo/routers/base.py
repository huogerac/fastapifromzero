from fastapi import APIRouter
from fastapi.exceptions import RequestValidationError

from todo.exceptions import BusinessError, UnauthorizedException
from todo.schemas.base import Error

router = APIRouter()


@router.get(
    "/dapau",
    status_code=503,
    response_model=Error,
    responses={
        400: {"model": Error, "description": "Business Error"},
        401: {"model": Error},
        422: {"model": Error, "description": "Bad Request"},
        503: {"model": Error},
    },
)
async def dapau(error: str | None = None):
    """
    Retorna um erro real para ajudar nos testes\n
    **Parameters**:\n
        - error (str): O tipo do erro que será lancado, Exemplo: Business, Unauthorized
    **Returns**:\n
        - Um Erro de propósito
    """
    if error and error.upper() == "BUSINESS":
        raise BusinessError("Erro de negócio de propósito")
    elif error and error.upper() == "UNAUTHORIZED":
        raise UnauthorizedException("BusinessError de propósito")
    elif error and error.upper() == "BADREQUEST":
        raise RequestValidationError("Input inválido de propósito")

    raise Exception("Erro interno de propósito")


@router.get("/status", response_model=dict)
async def get_status():
    """
    Retorna o estado atual da aplicação
    """

    response = {
        "status": "ok",
    }
    return response
