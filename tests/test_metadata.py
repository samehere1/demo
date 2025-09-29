# tests/test_metadata.py
import os
from fastapi.testclient import TestClient
from app.main import app

def test_healthz():
    client = TestClient(app)
    r = client.get("/healthz")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"

def test_metadata():
    client = TestClient(app)
    r = client.get("/v1/metadata")
    assert r.status_code == 200
    body = r.json()
    assert "model_version" in body
    # Artifacts may not exist in CI; ensure keys are present
    assert "artifacts_present" in body
