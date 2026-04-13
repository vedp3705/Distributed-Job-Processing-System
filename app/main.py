from fastapi import FastAPI
import uuid
import time

from app.queue_system import job_queue, results, start_workers
from app.models import JobRequest
from app.logger import logger

app = FastAPI()

start_workers(5)


@app.post("/submit")
def submit_job(req: JobRequest):
    job_id = str(uuid.uuid4())
    trace_id = str(uuid.uuid4())

    job = {
        "id": job_id,
        "trace_id": trace_id,
        "data": req.data,
        "retries": 0,
        "created_at": time.time()
    }

    results[job_id] = {"status": "queued"}
    job_queue.put(job)

    logger.info(f"[Trace {trace_id}] Job submitted {job_id}")

    return {"job_id": job_id, "trace_id": trace_id}


@app.get("/status/{job_id}")
def get_status(job_id: str):
    return results.get(job_id, {"error": "Job not found"})
