from datetime import datetime

from sqlalchemy import func, String, ForeignKey
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


@table_registry.mapped_as_dataclass
class UserSession:
    __tablename__ = "auth_sessions"

    session_id: Mapped[str] = mapped_column(String(32), primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("auth_users.id"), index=True)
    expire_at: Mapped[datetime] = mapped_column(init=False, server_default=func.now())

    def __repr__(self) -> str:
        return f"<Session {self.id}: {self.user_id}>"

    def to_dict_json(self):
        return {
            "session_id": self.session_id,
            "user_id": self.user_id,
            "expire_at": self.expire_at.isoformat() if self.expire_at else None,
        }
