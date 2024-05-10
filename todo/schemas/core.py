from pydantic import BaseModel, ConfigDict


class TaskSchema(BaseModel):
    id: str
    description: str

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 42,
                "description": "Task One",
            }
        },
    )
