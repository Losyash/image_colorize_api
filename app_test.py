from fastapi.testclient import TestClient
from app import app

client = TestClient(app)


def test_read_summarize_none_body():
    response = client.post("/api/file", json=None)

    assert response.status_code == 422


def test_read_summarize_none_text():
    response = client.post("/api/file", json={"file": None})

    assert response.status_code == 422
