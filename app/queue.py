import redis
import json
from app.config import REDIS_HOST, REDIS_PORT

r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

QUEUE_NAME = "job_queue"


def enqueue(job: dict):
    r.lpush(QUEUE_NAME, json.dumps(job))


def dequeue():
    _, job = r.brpop(QUEUE_NAME)
    return json.loads(job)


def get_queue_size():
    return r.llen(QUEUE_NAME)