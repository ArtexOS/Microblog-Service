import os
from fastapi.testclient import TestClient
from app.main import app
from app.config import settings

client = TestClient(app)

def test_root():
    r = client.get("/")
    assert r.status_code in (200, 404)

def test_unauthorized():
    r = client.get("/api/tweets")
    assert r.status_code == 422 or r.status_code == 401  # missing or invalid api-key

def test_docs_available():
    r = client.get("/docs")
    assert r.status_code == 200
