from datetime import datetime
from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column, registry

# from todo.database import Base

table_registry = registry()


@table_registry.mapped_as_dataclass
class Task:
    __tablename__ = "core_tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    description: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(init=False, server_default=func.now())

    def __repr__(self) -> str:
        return f"<Task {self.id}: {self.description}>"
