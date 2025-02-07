from pydantic import BaseModel


class ProjectCreateDTO(BaseModel):
    name: str
    description: str
    organization_id: int
    creator_id: int


class ProjectUpdateDTO(BaseModel):
    name: str
    description: str
