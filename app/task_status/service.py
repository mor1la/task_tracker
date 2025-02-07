from sqlalchemy import select, insert, update, delete
from app.db import async_session_maker
from app.task_status.model import TaskStatus  # Убедитесь, что путь импорта корректен
from app.exceptions import TASK_STATUS_ALREADY_EXISTS, TASK_STATUS_NOT_FOUND  # Создайте соответствующие исключения

class TaskStatusService:
    model = TaskStatus

    @classmethod
    async def create_task_status(cls, name: str, description: str | None) -> TaskStatus:
        async with async_session_maker() as session:
            existing_status = await cls.find_task_status_by_name(name)
            if existing_status:
                raise TASK_STATUS_ALREADY_EXISTS

            query = insert(cls.model).values(name=name, description=description)
            await session.execute(query)
            await session.commit()

            return await cls.find_task_status_by_name(name)

    @classmethod
    async def update_task_status(cls, task_status_id: int, name: str | None, description: str | None):
        async with async_session_maker() as session:
            existing_status = await cls.find_task_status_by_id(task_status_id)
            if not existing_status:
                raise TASK_STATUS_NOT_FOUND

            query = (
                update(cls.model)
                .where(cls.model.id == task_status_id)
                .values(name=name or existing_status.name, description=description or existing_status.description)
            )
            await session.execute(query)
            await session.commit()
            return await cls.find_task_status_by_id(task_status_id)

    @classmethod
    async def delete_task_status(cls, task_status_id: int):
        async with async_session_maker() as session:
            query = delete(cls.model).where(cls.model.id == task_status_id)
            result = await session.execute(query)
            if result.rowcount == 0:
                raise TASK_STATUS_NOT_FOUND
            await session.commit()

    @classmethod
    async def find_task_status_by_id(cls, task_status_id: int):
        async with async_session_maker() as session:
            query = select(cls.model).where(cls.model.id == task_status_id)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def find_task_status_by_name(cls, name: str):
        async with async_session_maker() as session:
            query = select(cls.model).where(cls.model.name == name)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def list_all_task_statuses(cls):
        async with async_session_maker() as session:
            query = select(cls.model)
            result = await session.execute(query)
            return result.scalars().all()