from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class UserRegisterDTO(BaseModel):
    email: EmailStr
    username: str
    password: str


class UserLoginDTO(BaseModel):
    email: EmailStr
    password: str
