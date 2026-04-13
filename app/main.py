from fastapi import FastAPI
import uuid
import time

from app.schemas import JobRequest
from app.queue import enqueue, get_queue_size
from app.tracing import generate_trace_id
from app.metrics import get_metrics
from app.logger import logger

app = FastAPI()


@app.post("/submit")
def submit_job(req: JobRequest):
    job_id = str(uuid.uuid4())
    trace_id = generate_trace_id()

    job = {
        "job_id": job_id,
        "trace_id": trace_id,
        "task": req.task,
        "payload": req.payload,
        "retries": 0,
        "created_at": time.time()
    }

    enqueue(job)

    logger.info(f"[Trace {trace_id}] Job submitted {job_id}")

    return {"job_id": job_id, "trace_id": trace_id, "status": "queued"}


@app.get("/metrics")
def metrics():
    return get_metrics(get_queue_size())