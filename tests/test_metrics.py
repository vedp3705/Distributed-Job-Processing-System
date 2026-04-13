from app.metrics import record_success, record_failure, get_metrics


def test_metrics_tracking():
    record_success(0.1)
    record_success(0.2)
    record_failure()

    metrics = get_metrics(queue_size=2)

    assert metrics["total_jobs"] >= 3
    assert metrics["successful_jobs"] >= 2
    assert metrics["failed_jobs"] >= 1
    assert metrics["average_latency_ms"] > 0