from typing import List, Optional
from pydantic import BaseModel, ConfigDict, ValidationInfo, field_validator


class UserSchema(BaseModel):
    id: Optional[str]
    username: str
    email: str
    name: Optional[str]
    created_at: str

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 42,
                "username": "john",
                "email": "john@example.com",
                "name": "Jõao Silva",
                "created_at": "2024-05-11T14:14:51.915183",
            }
        },
    )


class TaskSchemaIn(BaseModel):
    description: str
    username: str
    email: str
    password: str
    name: str

    @field_validator("password")
    def valid_password(cls, password: str, info: ValidationInfo) -> str:
        if password and len(password) < 6:
            raise ValueError("Password lenght must be at least 6 characteres long.")
        return password


class ListUsersSchema(BaseModel):
    tasks: List[UserSchema]
