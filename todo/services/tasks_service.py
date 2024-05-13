from todo.exceptions import BusinessError
from todo.models.core import Task


def list_tasks(session) -> list:
    # logger.info("SERVICE list tasks")
    tasks_list = session.query(Task).all()
    return [item.to_dict_json() for item in tasks_list]


def add_task(session, new_task: str) -> dict:
    # logger.info("SERVICE add new task")
    if not isinstance(new_task, str):
        raise BusinessError("Invalid description")

    if not new_task or not new_task.strip():
        raise BusinessError("Invalid description")

    task = Task(
        id=None,
        description=new_task,
    )
    session.add(task)
    session.commit()
    session.refresh(task)

    # logger.info(f"SERVICE task created.")
    return task.to_dict_json()
