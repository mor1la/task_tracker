from pydantic import BaseModel
from enum import Enum

class RoleEnumDTO(str, Enum):
    WORKER = "WORKER"
    ADMIN = "ADMIN"
    ORGANIZATION_CREATOR = "ORGANIZATION_CREATOR"

class RoleCreateDTO(BaseModel):
    name: RoleEnumDTO
    description: str

class RoleUpdateDTO(BaseModel):
    name: RoleEnumDTO
    description: str
