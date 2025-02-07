from sqlalchemy import Column, Integer, String
from app.db import Base
from sqlalchemy.orm import relationship
from enum import Enum

class RoleEnum(int, Enum):
    WORKER = 0
    ADMIN = 1
    CREATOR = 2

class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=False)

    users = relationship("Users", back_populates="role")
