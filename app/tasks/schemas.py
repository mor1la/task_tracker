from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class TaskResponseSchema(BaseModel):
    id: int
    title: str
    description: Optional[str]
    created_at: Optional[str]
    updated_at: Optional[str]
    deadline: Optional[str]
    project_id: int
    assignee_id: Optional[int]
    status: str
    completed: Optional[bool]

    class Config:
        orm_mode = True

class TaskCreateSchema(BaseModel):
    title: str
    description: Optional[str] = None
    created_at: Optional[datetime] = None
    status: Optional[str] = None

    class Config:
        orm_mode = True
