from fastapi import status


def test_deve_retornar_404_not_found_para_url_invalida(client):
    # Quando tentamos acessar
    resp = client.get("/api/core/invalid/url")

    # Entao 404
    assert resp.status_code == status.HTTP_404_NOT_FOUND
