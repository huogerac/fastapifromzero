import mock
from unittest.mock import ANY
from fastapi import status

from tests.conftest import userMock
from todo.models.core import Task


def test_nao_deve_permitir_listar_task_sem_login(client):
    # Quando adicionamos um item
    response = client.get(
        "/api/core/tasks/list/",
    )

    # Entao
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_deve_retornar_lista_vazia(client, session):

    # Retorna um usuário logado
    with mock.patch("tests.conftest.get_session_and_user_for_tests") as get_session_user_mock:
        get_session_user_mock.return_value = ("session-mock", userMock)

        # Quando tentamos listar itens
        resp = client.get("/api/core/tasks/list")
        data = resp.json()

        # Entao recebemos um sem autorizacao
        assert resp.status_code == 200
        assert data.get("tasks") == []


def test_deve_listar_task_com_login(client, session):
    # Dado um item criado
    new_task = Task(id=100, description="walk the dog")
    session.add(new_task)
    session.commit()

    # Retorna um usuário logado
    with mock.patch("tests.conftest.get_session_and_user_for_tests") as get_session_user_mock:
        get_session_user_mock.return_value = ("session-mock", userMock)

        # Quando listamos
        resp = client.get("/api/core/tasks/list")
        data = resp.json()

        # Entao
        assert resp.status_code == 200
        assert data == {
            "tasks": [{"description": "walk the dog", "created_at": ANY, "id": ANY}]
        }
