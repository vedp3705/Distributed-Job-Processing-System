import threading
import queue
import time
import random

from app.metrics import metrics
from app.logger import logger

job_queue = queue.Queue()
results = {}
lock = threading.Lock()

MAX_RETRIES = 3


def process_job(job):
    time.sleep(random.uniform(0.05, 0.2))

    if random.random() < 0.2:
        raise Exception("Random failure")

    return f"Processed: {job['data']}"


def worker(worker_id):
    while True:
        job = job_queue.get()
        job_id = job["id"]
        trace_id = job["trace_id"]

        start_time = time.time()

        try:
            logger.info(f"[Trace {trace_id}] Worker {worker_id} processing {job_id}")

            result = process_job(job)

            with lock:
                results[job_id] = {
                    "status": "completed",
                    "result": result,
                    "latency": time.time() - start_time
                }
                metrics["success"] += 1

        except Exception as e:
            if job["retries"] < MAX_RETRIES:
                job["retries"] += 1
                logger.warning(f"[Trace {trace_id}] Retry {job_id}")
                job_queue.put(job)
            else:
                with lock:
                    results[job_id] = {
                        "status": "failed",
                        "error": str(e)
                    }
                    metrics["failed"] += 1

        finally:
            with lock:
                metrics["total_jobs"] += 1

            job_queue.task_done()


def start_workers(n=4):
    for i in range(n):
        t = threading.Thread(target=worker, args=(i,), daemon=True)
        t.start()
