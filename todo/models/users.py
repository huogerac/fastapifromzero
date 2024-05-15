from datetime import datetime
from sqlalchemy import func, String
from sqlalchemy.orm import Mapped, mapped_column

from todo.database import table_registry


@table_registry.mapped_as_dataclass
class User:
    __tablename__ = "auth_users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(128), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(1024), nullable=True)
    email: Mapped[str] = mapped_column(String(256), unique=True, nullable=True)
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    created_at: Mapped[datetime] = mapped_column(init=False, server_default=func.now())

    def __repr__(self) -> str:
        return f"<User {self.id}: {self.username}>"

    def to_dict_json(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "name": self.name,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
