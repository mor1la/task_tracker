from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db import Base

class TaskStatus(Base):
    __tablename__ = "task_status"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)

    tasks = relationship("Task", back_populates="status")
