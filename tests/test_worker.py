import pytest
from app.worker import process_job


def test_process_job_success(monkeypatch):
    monkeypatch.setattr("random.random", lambda: 0.9)

    job = {"data": "hello"}
    result = process_job(job)

    assert result is not None


def test_process_job_failure(monkeypatch):
    monkeypatch.setattr("random.random", lambda: 0.1)

    job = {"data": "fail"}

    with pytest.raises(Exception):
        process_job(job)