import time
import random
from app.queue import dequeue, enqueue
from app.metrics import record_success, record_failure
from app.logger import logger

MAX_RETRIES = 3


def process_job(job):
    time.sleep(random.uniform(0.05, 0.2))

    if random.random() < 0.2:
        raise Exception("Random failure")

    return {"message": "success"}


def worker():
    while True:
        job = dequeue()
        start = time.time()

        try:
            logger.info(f"[Trace {job['trace_id']}] Processing {job['job_id']}")

            result = process_job(job)

            latency = time.time() - start
            record_success(latency)

        except Exception as e:
            if job["retries"] < MAX_RETRIES:
                job["retries"] += 1
                time.sleep(2 ** job["retries"])
                enqueue(job)
                logger.warning(f"Retry {job['job_id']}")
            else:
                record_failure()
                logger.error(f"Failed {job['job_id']}: {str(e)}")


if __name__ == "__main__":
    worker()