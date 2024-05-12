from fastapi import status


def test_core_status(client):
    """First test"""
    response = client.get("/api/core/status")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"status": "ok"}


def test_swagger_docs(client):
    """Test the docs is working"""
    response = client.get("/docs")
    assert response.status_code == status.HTTP_200_OK
