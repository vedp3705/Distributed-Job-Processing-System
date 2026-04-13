
import uuid
from sqlalchemy import Column, String, Integer, JSON, TIMESTAMP
from app.database import Base


class Job(Base):
    __tablename__ = "jobs"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    trace_id = Column(String, nullable=False)
    task_type = Column(String)
    status = Column(String)
    payload = Column(JSON)
    result = Column(JSON)
    retries = Column(Integer, default=0)
    latency_ms = Column(Integer)
    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)