from pydantic import BaseModel


class JobRequest(BaseModel):
    data: str
