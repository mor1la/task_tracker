from pydantic import BaseModel


class OrganizationCreateDTO(BaseModel):
    name: str
    description: str


class OrganizationUpdateDTO(BaseModel):
    name: str
    description: str
