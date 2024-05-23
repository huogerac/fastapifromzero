import mock
from unittest.mock import ANY
from fastapi import status

from tests.conftest import userMock
from todo.exceptions import BusinessError


def test_nao_deve_permitir_criar_task_sem_login(client):
    # Dado um usuario logado
    payload = {"description": "estudar pytest"}

    # Quando adicionamos um item
    response = client.post(
        "/api/core/tasks/add/",
        json=payload,
    )

    # Entao
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_deve_criar_nova_task(client, session):

    # Retorna um usuário logado
    with mock.patch("tests.conftest.get_session_and_user_for_tests") as get_session_user_mock:
        get_session_user_mock.return_value = ("session-mock", userMock)

        # Dado um usuario logado
        payload = {"description": "estudar pytest"}

        # Quando adicionamos um item
        response = client.post(
            "/api/core/tasks/add/",
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
        "/api/core/tasks/add",
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
        "/api/core/tasks/add/",
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
        "/api/core/tasks/add/",
        json=payload,
    )

    # Então
    assert resp.status_code == 422
    assert resp.json() == {
        "message": "[INVALID INPUT] body.description: Input should be a valid string (string_type)",
    }


def test_deve_receber_erro_enviado_pela_classe_de_servico(client):

    # Retorna um usuário logado
    with mock.patch("tests.conftest.get_session_and_user_for_tests") as get_session_user_mock:
        get_session_user_mock.return_value = ("session-mock", userMock)

        # Dado uma entrada inválida
        payload = {"description": "INVALID DESCRIPTION"}

        # Quando tentamos adicionar
        with mock.patch("todo.services.tasks_service.add_task") as add_task_mock:
            add_task_mock.side_effect = BusinessError("Invalid description")
            resp = client.post(
                "/api/core/tasks/add/",
                json=payload,
            )
            msg = resp.json()

        # Então
        assert resp.status_code == 400
        assert msg == {"message": "[ERROR] Invalid description"}
