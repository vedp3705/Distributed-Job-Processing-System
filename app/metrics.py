metrics = {
    "total_jobs": 0,
    "success": 0,
    "failed": 0,
    "latencies": []
}


def record_success(latency):
    metrics["total_jobs"] += 1
    metrics["success"] += 1
    metrics["latencies"].append(latency)


def record_failure():
    metrics["total_jobs"] += 1
    metrics["failed"] += 1


def get_metrics(queue_size):
    avg_latency = (
        sum(metrics["latencies"]) / len(metrics["latencies"])
        if metrics["latencies"] else 0
    )

    success_rate = (
        metrics["success"] / metrics["total_jobs"]
        if metrics["total_jobs"] else 0
    )

    return {
        "queue_size": queue_size,
        "total_jobs": metrics["total_jobs"],
        "successful_jobs": metrics["success"],
        "failed_jobs": metrics["failed"],
        "average_latency_ms": avg_latency * 1000,
        "success_rate": success_rate
    }