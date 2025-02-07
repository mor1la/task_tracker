from typing import Optional

from fastapi import HTTPException
from sqlalchemy import select, update, delete
from app.db import async_session_maker
from app.tasks.DTO import TaskUpdateDTO
from app.tasks.model import Task
from datetime import datetime

from sqlalchemy.orm import selectinload

from app.tasks.schemas import TaskResponseSchema


class TaskService:

    model = Task

    @classmethod
    async def create_task(cls, title: str, description: Optional[str], deadline: Optional[datetime], project_id: int,
                          assignee_id: Optional[int]) -> TaskResponseSchema:
        async with async_session_maker() as session:
            new_task = cls.model(title=title, description=description, deadline=deadline, project_id=project_id,
                                 assignee_id=assignee_id)
            session.add(new_task)
            await session.commit()
            await session.refresh(new_task)
            created_str = new_task.created_at.strftime('%Y-%m-%d %H:%M:%S') if new_task.created_at else None
            status_string = await cls.get_status_string(new_task.status_id)

            return TaskResponseSchema(
                id=new_task.id,
                title=new_task.title,
                description=new_task.description,
                created_at=created_str,
                updated_at=None,
                deadline=None,
                project_id=new_task.project_id,
                assignee_id=new_task.assignee_id,
                status=status_string,
                completed=None
            )

    @classmethod
    async def get_status_string(cls, status_id: int) -> str:
        status_mapping = {
            1: "pending",
            2: "in_progress",
            3: "completed",
        }
        return status_mapping.get(status_id, "unknown")

    @classmethod
    async def get_task_by_id(cls, task_id: int) -> TaskResponseSchema:
        async with async_session_maker() as session:
            query = select(cls.model).where(cls.model.id == task_id)
            result = await session.execute(query)
            task = result.scalar_one_or_none()
            if not task:
                raise HTTPException(status_code=404, detail="Task not found")

            return TaskResponseSchema(
                id=task.id,
                title=task.title,
                description=task.description,
                created_at=task.created_at.strftime('%Y-%m-%d %H:%M:%S') if task.created_at else None,
                updated_at=task.updated_at.strftime('%Y-%m-%d %H:%M:%S') if task.updated_at else None,
                deadline=task.deadline.strftime('%Y-%m-%d %H:%M:%S') if task.deadline else None,
                project_id=task.project_id,
                assignee_id=task.assignee_id,
                status=await cls.get_status_string(task.status_id) or "unknown",
                completed=task.completed,
            )

    @classmethod
    async def update_task(cls, task_id: int, task_data: TaskUpdateDTO) -> TaskResponseSchema:
        async with async_session_maker() as session:
            task = await session.get(cls.model, task_id)
            if not task:
                raise HTTPException(status_code=404, detail="Task not found")

            for key, value in task_data.dict(exclude_unset=True).items():
                setattr(task, key, value)

            await session.commit()

            return await cls.get_task_by_id(task_id)

    @classmethod
    async def delete_task(cls, task_id: int):
        async with async_session_maker() as session:
            query = delete(cls.model).where(cls.model.id == task_id)
            result = await session.execute(query)
            await session.commit()

            if result.rowcount == 0:
                raise HTTPException(status_code=404, detail="Task not found")
