from sqlalchemy import Column, Integer, String
from app.db import Base
from sqlalchemy.orm import relationship

class Organization(Base):
    __tablename__ = "organizations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=False)

    projects = relationship("Project", back_populates="organization")
    users = relationship("Users", secondary="user_organizations", back_populates="organizations")
