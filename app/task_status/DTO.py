from pydantic import BaseModel

class TaskStatusCreateDTO(BaseModel):
    name: str
    description: str | None = None


class TaskStatusUpdateDTO(BaseModel):
    name: str | None = None
    description: str | None = None