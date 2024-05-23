from pydantic import BaseModel, ConfigDict


class Error(BaseModel):
    message: str

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "message": "[INVALID INPUT] Campo body.email é obrigatório",
            }
        },
    )
