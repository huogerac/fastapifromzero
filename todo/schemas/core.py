from typing import List, Optional
from pydantic import BaseModel, ConfigDict, ValidationInfo, field_validator


class TaskSchema(BaseModel):
    id: Optional[str]
    description: str
    created_at: str

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 42,
                "description": "Task One",
                "created_at": "2024-05-11T14:14:51.915183",
            }
        },
    )


class TaskSchemaIn(BaseModel):
    description: str

    @field_validator("description")
    def valid_description(cls, description: str, info: ValidationInfo) -> str:
        if description and len(description) <= 2:
            raise ValueError("It must be at least 3 characteres long.")
        return description


class ListTasksSchema(BaseModel):
    tasks: List[TaskSchema]
