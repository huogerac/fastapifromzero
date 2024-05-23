from typing import Optional
from pydantic import BaseModel, ConfigDict


class UserSchema(BaseModel):
    id: Optional[int]
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


class LoginSchema(BaseModel):
    email: str
    password: str

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "email": "john@example.com",
                "password": "abacate",
            }
        },
    )


class LoggedUserSchema(BaseModel):
    authenticated: bool
    user: Optional[UserSchema] = None
