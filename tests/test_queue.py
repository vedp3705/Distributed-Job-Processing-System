from app.queue import enqueue, dequeue


def test_queue_enqueue_dequeue(fake_queue):
    job = {"id": "1"}

    fake_queue.enqueue(job)
    result = fake_queue.dequeue()

    assert result == job