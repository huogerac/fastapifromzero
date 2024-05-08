from fastapi.testclient import TestClient
from fastapi import status

from todo.main import app

client = TestClient(app)


def test_core_status():
    """First test"""
    response = client.get("/api/core/status")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"status": "ok"}


def test_swagger_docs():
    """Test the docs is working"""
    response = client.get("/docs")
    assert response.status_code == status.HTTP_200_OK
