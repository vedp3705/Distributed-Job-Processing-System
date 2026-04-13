from pydantic import BaseModel
from typing import Dict, Any


class JobRequest(BaseModel):
    task: str
    payload: Dict[str, Any]