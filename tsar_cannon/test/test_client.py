import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def test_app():
    from ..main import app
    return app


@pytest.fixture
def test_client(test_app):
    return TestClient(test_app)


@pytest.fixture
def sample_client_data():
    return {
        "fio": "Test Client",
        "login": "test",
        "password": "test"
    }


def test_post(test_client, sample_client_data):

    resp = test_client.post("/api/client/", json=sample_client_data)
    assert resp.status_code == 201

def test_get_list(test_client):
    resp = test_client.get(f"/api/client/list?skip=0&limit=100")
    assert resp.status_code == 200

def test_get(test_client, sample_client_data):
    resp = test_client.get(f"/api/client/?client_login={sample_client_data["login"]}")
    assert resp.status_code == 200

def test_delete(test_client, sample_client_data):
    resp = test_client.delete(f"/api/client/?client_login={sample_client_data["login"]}")
    assert resp.status_code == 204


