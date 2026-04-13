from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_submit_and_status():
    response = client.post("/submit", json={"data": "test"})
    assert response.status_code == 200

    job_id = response.json()["job_id"]

    status_response = client.get(f"/status/{job_id}")
    assert status_response.status_code == 200
