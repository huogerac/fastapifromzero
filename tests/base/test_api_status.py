from unittest.mock import ANY
from fastapi import status


def test_obter_status(client):
    resp = client.get("/api/status")

    assert resp.status_code == status.HTTP_200_OK
    assert resp.json() == {
        "status": "ok",
    }


def test_swagger_docs(client):
    """Test the docs is working"""
    response = client.get("/api/docs")

    assert response.status_code == status.HTTP_200_OK
