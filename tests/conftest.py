import pytest
from fastapi.testclient import TestClient
from app.main import app

# Fake in-memory queue
class FakeQueue:
    def __init__(self):
        self.q = []

    def enqueue(self, job):
        self.q.insert(0, job)

    def dequeue(self):
        return self.q.pop()

    def size(self):
        return len(self.q)


@pytest.fixture
def client(monkeypatch):
    fake_queue = FakeQueue()

    # Mock queue functions
    monkeypatch.setattr("app.queue.enqueue", fake_queue.enqueue)
    monkeypatch.setattr("app.queue.get_queue_size", fake_queue.size)

    return TestClient(app)


@pytest.fixture
def fake_queue(monkeypatch):
    q = FakeQueue()
    monkeypatch.setattr("app.queue.enqueue", q.enqueue)
    monkeypatch.setattr("app.queue.dequeue", q.dequeue)
    return q
