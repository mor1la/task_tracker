from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class TaskCreateDTO(BaseModel):
    title: str
    description: Optional[str] = None
    created_at: Optional[datetime] = None
    project_id: int
    assignee_id: Optional[int] = None


class TaskUpdateDTO(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    created_at: Optional[datetime] = None
    status: Optional[str] = None
    assignee_id: Optional[int] = None
    completed: Optional[bool] = None


class TaskDTO(BaseModel):
    id: int
    title: str
    description: Optional[str]
    created_at: datetime
    updated_at: datetime
    deadline: Optional[datetime]
    status: str
    assignee_id: Optional[int]
    project_id: int
    completed: bool

    class Config:
        orm_mode = True
