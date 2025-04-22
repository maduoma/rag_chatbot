import pytest
from fastapi.testclient import TestClient
from app.api.main import app

client = TestClient(app)

def test_chat_endpoint():
    response = client.post('/chat', json={'query': 'hello'})
    assert response.status_code == 200
    assert 'answer' in response.json()

def test_upload_endpoint():
    # This test should use a real or mock file
    assert True  # Placeholder
