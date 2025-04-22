import pytest
from app.ui.flask_app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home_page(client):
    resp = client.get('/', follow_redirects=True)
    assert resp.status_code == 200
    assert b'RAG Chatbot' in resp.data

def test_upload_page(client):
    resp = client.get('/upload')
    assert resp.status_code == 200
    assert b'Upload' in resp.data
