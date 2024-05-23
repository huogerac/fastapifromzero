from sqlalchemy import select

from todo.models.core import Task


def test_create_task(session):
    new_task = Task(id=100, description="Task One")
    session.add(new_task)
    session.commit()

    task = session.scalar(select(Task).where(Task.description == "Task One"))

    assert task.id == 100
    assert task.description == "Task One"
