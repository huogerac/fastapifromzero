import mock
from unittest.mock import ANY

from tests.conftest import userMock
from todo.services.auth_service import get_password_hash
from todo.models.users import User


def test_deve_retornar_usuario_nao_logado(client):

    resp = client.get("/api/accounts/whoami")

    assert resp.status_code == 200
    assert resp.json() == {"authenticated": False}


def test_deve_fazer_login(session, client):

    new_user = User(
        id=None,
        username="jon",
        email="jon@doe.com.br",
        name="Jon Doe",
        password=get_password_hash("abacate"),
    )

    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    payload = {"email": "jon@doe.com.br", "password": "abacate"}
    resp = client.post("/api/accounts/login", json=payload)
    login = resp.json()

    assert resp.status_code == 201
    assert login["email"] == "jon@doe.com.br"
    assert login["name"] == "Jon Doe"


def test_deve_retornar_usuario_logado(client):


    with mock.patch("tests.conftest.get_session_and_user_for_tests") as get_session_user_mock:
        get_session_user_mock.return_value = ("session-mock", userMock)

        resp = client.get("/api/accounts/whoami")
        data = resp.json()

        user_data = userMock.to_dict_json()
        assert resp.status_code == 200
        assert data == {
            "user": {
                "id": user_data['id'],
                'username': user_data['username'],
                "email": user_data['email'],
                "name": user_data['name'],
                "created_at": user_data['created_at'],
            },
            "authenticated": True,
        }
