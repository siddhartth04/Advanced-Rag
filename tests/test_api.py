import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def client():
    from rag.api.main import app

    return TestClient(app)


def test_health(client):
    """Test health endpoint """
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "llm_model" in data


@pytest.mark.asyncio
async def test_query_non_streaming(client, mock_litellm):
    """Test non-streaming query."""
    response = client.post(
        "/query",
        json={"question": "What is Axonify?", "stream": False},
    )
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    assert "node_path" in data


def test_eval_latest(client):
    """Test eval latest endpoint."""
    response = client.get("/eval/latest")
    assert response.status_code == 200
    data = response.json()
    assert "faithfulness" in data
    assert "answer_relevancy" in data
