import mock
from unittest.mock import ANY
from fastapi import status

from todo.exceptions import BusinessError


def test_nao_deve_permitir_criar_task_sem_login():
    pass


def test_deve_criar_nova_task(client, session):
    # Dado um usuario logado
    payload = {"description": "estudar pytest"}

    # Quando adicionamos um item
    response = client.post(
        "/api/core/tasks/",
        headers={},
        json=payload,
    )

    # Entao
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == {
        "id": ANY,
        "description": "estudar pytest",
        "created_at": ANY,
    }


def test_deve_falhar_com_input_invalido(client):
    # Dado uma entrada inválida
    payload = {}

    # Quando tentamos adicionar
    resp = client.post(
        "/api/core/tasks",
        json=payload,
    )
    msg = resp.json()

    # Então
    assert resp.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY  # BAD REQUEST
    assert msg == {
        "message": "[INVALID INPUT] body.description: Field required (missing)",
    }


def test_deve_falhar_com_input_menor_que_minimo_necessario(client):
    # Dado uma entrada inválida
    payload = {"description": "??"}

    # Quando tentamos adicionar
    resp = client.post(
        "/api/core/tasks/",
        json=payload,
    )

    # Então
    assert resp.status_code == 422  # BAD REQUEST
    assert resp.json() == {
        "message": "[INVALID INPUT] body.description: Value error, It must be at least 3 characteres long. (value_error)",
    }


def test_deve_falhar_quando_description_contem_algo_diferente_de_string(client):
    # Dado uma entrada inválida
    payload = {"description": {"objeto": "invalido"}}

    # Quando tentamos adicionar
    resp = client.post(
        "/api/core/tasks/",
        json=payload,
    )

    # Então
    assert resp.status_code == 422
    assert resp.json() == {
        "message": "[INVALID INPUT] body.description: Input should be a valid string (string_type)",
    }


def test_deve_receber_erro_enviado_pela_classe_de_servico(client):
    # Dado uma entrada inválida
    payload = {"description": "INVALID DESCRIPTION"}

    # Quando tentamos adicionar
    with mock.patch("todo.services.tasks_service.add_task") as add_task_mock:
        add_task_mock.side_effect = BusinessError("Invalid description")
        resp = client.post(
            "/api/core/tasks/",
            json=payload,
        )
        msg = resp.json()

    # Então
    assert resp.status_code == 400
    assert msg == {"message": "[ERROR] Invalid description"}
