from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db import Base

class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=True)

    organizations = relationship("Organization", secondary="user_organizations", back_populates="users")
    role = relationship("Role", back_populates="users")
    tasks = relationship("Task", back_populates="assigned_user")
    created_projects = relationship("Project", back_populates="creator")


class UserOrganizations(Base):
    __tablename__ = "user_organizations"

    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    organization_id = Column(Integer, ForeignKey('organizations.id'), primary_key=True)
