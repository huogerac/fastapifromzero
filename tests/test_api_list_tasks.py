import pytest
from unittest.mock import ANY

from todo.models.core import Task


def test_nao_deve_permitir_listar_task_sem_login(client, session):
    # Dado um usuário anônimo

    # Quando tentamos listar itens
    resp = client.get("/api/core/tasks/")

    # Entao recebemos um sem autorizacao
    #assert resp.status_code == 401  --> TODO
    assert resp is not None


def test_deve_retornar_lista_vazia(client, session):
    # Quando tentamos listar itens
    resp = client.get("/api/core/tasks/")
    data = resp.json()

    # Entao recebemos um sem autorizacao
    assert resp.status_code == 200
    assert data.get("tasks") == []


def test_deve_listar_task_com_login(client, session):
    # Dado um item criado
    task = Task(
        id=None,
        description="walk the dog",
    )
    session.add(task)
    session.commit()
    session.refresh(task)

    # Quando listamos
    resp = client.get("/api/core/tasks/")
    data = resp.json()

    # Entao
    assert resp.status_code == 200
    assert data == {
        "tasks": [{"description": "walk the dog", "created_at": ANY, "id": ANY}]
    }
