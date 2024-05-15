from datetime import datetime
from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column

from todo.database import table_registry


@table_registry.mapped_as_dataclass
class Task:
    __tablename__ = "core_tasks"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    description: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(init=False, server_default=func.now())

    def __repr__(self) -> str:
        return f"<Task {self.id}: {self.description}>"

    def to_dict_json(self):
        return {
            "id": str(self.id),
            "description": self.description,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
