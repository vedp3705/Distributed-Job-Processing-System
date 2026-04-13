def test_submit_job(client):
    response = client.post("/submit", json={
        "task": "test",
        "payload": {"x": 1}
    })

    assert response.status_code == 200
    data = response.json()

    assert "job_id" in data
    assert "trace_id" in data
    assert data["status"] == "queued"


def test_metrics_endpoint(client):
    response = client.get("/metrics")
    assert response.status_code == 200

    data = response.json()
    assert "queue_size" in data
    assert "total_jobs" in data